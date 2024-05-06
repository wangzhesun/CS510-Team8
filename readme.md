# Backend API
## analyze
**request url:** /analyze \
**request type:** POST \
**request body:**
| name | type |
| :-----------: | :-------------:| 
| query       |   string      | 

**request response:**
| name | type |
| :-----------: | :-------------:| 
| status       |   int      | 
| result       |   string      | 

**sample request body:**
{
    "query":"xxx"
} 

**sample request response:**
on success: {
    "status":0,
    "result": "xxx
}; 
on failure: {
    "status": 1,
    "result": "fail"
}

# Frontend
Before running the front end, please first ensure that the backend, that is, backend/app.py is running normally.
## how to use
1. please run ``pip install -r requirement.txt`` at first
2. run ``streamlit run frontend.py``