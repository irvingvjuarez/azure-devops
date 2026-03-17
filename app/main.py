from fastapi import FastAPI, HTTPException
from typing import List
from .models import Item

from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

import os

app = FastAPI()

connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")

trace.set_tracer_provider(TracerProvider())
tracer_provider = trace.get_tracer_provider()

exporter = AzureMonitorTraceExporter(
    connection_string=connection_string
)

span_processor = BatchSpanProcessor(exporter)
tracer_provider.add_span_processor(span_processor)

FastAPIInstrumentor.instrument_app(app)


@app.get("/")
def root():
    return {"message": "Hello telemetry"}

# In-memory "database"
items: List[Item] = []
current_id = 1

@app.get("/items", response_model=List[Item])
def get_items():
    return items


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/items", response_model=Item, status_code=201)
def create_item(item: Item):
    global current_id
    item.id = current_id
    current_id += 1
    items.append(item)
    return item


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(items):
        if item.id == item_id:
            updated_item.id = item_id
            items[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    for index, item in enumerate(items):
        if item.id == item_id:
            items.pop(index)
            return
    raise HTTPException(status_code=404, detail="Item not found")
