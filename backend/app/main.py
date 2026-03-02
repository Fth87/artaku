from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

# Model
class Transaction(BaseModel):
    id: Optional[int] = None
    description: str
    amount: float
    category: str
    type: str  # "income" or "expense"
    date: datetime = datetime.now()

# In-memory database
transactions_db: List[Transaction] = []
next_id = 1

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Money Tracking Backend!"}

# CREATE - Tambah transaksi baru
@app.post("/transactions", response_model=Transaction)
def create_transaction(transaction: Transaction):
    global next_id
    transaction.id = next_id
    next_id += 1
    transactions_db.append(transaction)
    return transaction

# READ - Ambil semua transaksi
@app.get("/transactions", response_model=List[Transaction])
def get_transactions():
    return transactions_db

# READ - Ambil transaksi berdasarkan ID
@app.get("/transactions/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: int):
    for transaction in transactions_db:
        if transaction.id == transaction_id:
            return transaction
    raise HTTPException(status_code=404, detail="Transaction not found")

# UPDATE - Update transaksi
@app.put("/transactions/{transaction_id}", response_model=Transaction)
def update_transaction(transaction_id: int, updated_transaction: Transaction):
    for index, transaction in enumerate(transactions_db):
        if transaction.id == transaction_id:
            updated_transaction.id = transaction_id
            transactions_db[index] = updated_transaction
            return updated_transaction
    raise HTTPException(status_code=404, detail="Transaction not found")

# DELETE - Hapus transaksi
@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int):
    for index, transaction in enumerate(transactions_db):
        if transaction.id == transaction_id:
            transactions_db.pop(index)
            return {"message": "Transaction deleted successfully"}
    raise HTTPException(status_code=404, detail="Transaction not found")