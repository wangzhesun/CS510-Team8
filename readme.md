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
