# Cargo-django

## Installation:   
```sudo docker-compose build```  
```sudo docker-compose up```  

## Paths :
- `/api/cargo`
  - `get` - Getting a list of cargo.  
  - `post` - Creating a new cargo.  
- `/api/cargo/<int:id>`
  - `get` - Obtaining information about a specific cargo.  
  - `put` - Editing cargo.  
  - `delete` - Cargo removal.  