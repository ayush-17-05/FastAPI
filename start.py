@app.get("/health")
def health_check():
    return {"status":"ok"}


items=[
    {"id":1,"name":"item1","price":10},
    {"id":2,"name":"item2","price":20},
    {"id":3,"name":"item3","price":30},
    {"id":4,"name":"item4","price":40},
]

@app.get("/items")
def get_items():
    return items


@app.get("/items/{item_id}")
def get_item(item_id:int):
    for item in items:
        if item["id"] == item_id:
            return item
        else:
            return {"error":"item not found"}

@app.post("/items")
def create_item(item:dict):
    items.append(item)
    return item