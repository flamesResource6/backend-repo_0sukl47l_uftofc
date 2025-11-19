import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

# Sample products endpoint for the fashion + accessories site
@app.get("/api/products")
def get_products():
    # Static showcase data for now (no persistence required yet)
    return {
        "items": [
            {
                "id": "ring-kintsugi",
                "name": "Kintsugi Ring",
                "price": 120,
                "currency": "USD",
                "category": "Jewelry",
                "color": "Brass / Porcelain",
                "image": "https://images.unsplash.com/photo-1523292562811-8fa7962a78c8?q=80&w=1200&auto=format&fit=crop",
                "badge": "Hand-mended",
                "desc": "Porcelain shard set in raw brass, gold-resined seams that honor the crack."
            },
            {
                "id": "tote-concrete",
                "name": "Concrete Tote",
                "price": 85,
                "currency": "USD",
                "category": "Bags",
                "color": "Ash Grey",
                "image": "https://images.unsplash.com/photo-1544025162-d76694265947?q=80&w=1200&auto=format&fit=crop",
                "badge": "Brut Minimal",
                "desc": "Heavy canvas with exposed stitching and oversized industrial webbing."
            },
            {
                "id": "scarf-moss",
                "name": "Moss Silk Scarf",
                "price": 65,
                "currency": "USD",
                "category": "Scarves",
                "color": "Moss / Stone",
                "image": "https://images.unsplash.com/photo-1520975922284-9e0ce8275ca6?q=80&w=1200&auto=format&fit=crop",
                "badge": "Naturally Dyed",
                "desc": "Hand-dyed with foraged pigments; tone variance embraced."
            },
            {
                "id": "boot-raw",
                "name": "Raw Edge Boot",
                "price": 240,
                "currency": "USD",
                "category": "Footwear",
                "color": "Char / Umber",
                "image": "https://images.unsplash.com/photo-1543508282-6319a3e2621f?q=80&w=1200&auto=format&fit=crop",
                "badge": "Unfinished Hem",
                "desc": "Sturdy leather with unapologetic seams and squared toe."
            },
            {
                "id": "bangle-patina",
                "name": "Patina Bangle",
                "price": 48,
                "currency": "USD",
                "category": "Jewelry",
                "color": "Oxidized Brass",
                "image": "https://images.unsplash.com/photo-1537183645340-1d0f2f2b5e1f?q=80&w=1200&auto=format&fit=crop",
                "badge": "Aged Finish",
                "desc": "Surface weathering varies; each piece tells its own story."
            },
            {
                "id": "cap-raw",
                "name": "Raw Canvas Cap",
                "price": 36,
                "currency": "USD",
                "category": "Headwear",
                "color": "Bone / Ink",
                "image": "https://images.unsplash.com/photo-1520975922284-9e0ce8275ca6?q=80&w=1200&auto=format&fit=crop",
                "badge": "Frayed Edge",
                "desc": "Unlined, adjustable, sun-softened look from day one."
            }
        ]
    }

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
