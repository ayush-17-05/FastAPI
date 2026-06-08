from fastapi import APIRouter, HTTPException, status
import uuid
from app.schemas import IssueCreate, IssueOut, IssuePriority, IssueStatus, IssueUpdate
from app.storage import save_data, load_data

router = APIRouter(prefix="/api/v1/issues", tags=["issues"])


@router.get("/", response_model=list[IssueOut])
async def get_issues():
    """Retrieve all issues."""
    issues = load_data()
    return issues

@router.post("/",response_model=IssueOut, status_code=status.HTTP_201_CREATED)
async def create_issue(payload: IssueCreate):
    """Create a new issue."""
    issues=load_data()
    new_issue={
        "id":str(uuid.uuid4()),
        "title":payload.title,
        "description":payload.description,
        "priority":payload.priority,
        "status":IssueStatus.open
    }
    issues.append(new_issue)
    save_data(issues)
    return new_issue

@router.get("/{issue_id}", response_model=IssueOut)
async def get_issue(issue_id: str):
    """Retrieve a single issue by ID."""
    issues = load_data()
    for issue in issues:
        if issue["id"] == issue_id:
            return issue
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Issue with ID '{issue_id}' not found",
    )


@router.put("/{issue_id}",response_model=IssueOut)
async def update_issue(issue_id:str, payload:IssueUpdate):
    """Update an existing issue."""
    issues=load_data()
    for index, issue in enumerate(issues):
        if issue["id"]==issue_id:
            updated_issue=issue.copy()
            if payload.title is not None:
                updated_issue["title"]=payload.title
            if payload.description is not None:
                updated_issue["description"]=payload.description
            if payload.priority is not None:
                updated_issue["priority"]=payload.priority
            if payload.status is not None:
                updated_issue["status"]=payload.status
            issues[index]=updated_issue
            save_data(issues)
            return updated_issue
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Issue with ID '{issue_id}' not found",
    )

@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_issue(issue_id: str):
    """Delete an existing issue."""
    issues=load_data()
    for index,issue in enumerate(issues):
        if issue["id"]==issue_id:
            issues.pop(index)
            save_data(issues)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Issue with ID '{issue_id}' not found",
    )