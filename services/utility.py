def sqlalchemy_to_pydantic_dict(obj, _depth=0, max_depth=2):
    """
    Convert SQLAlchemy model instances (like Youth or Karyakarta) to dictionaries 
    that can be used with Pydantic's model_validate method.
    
    Args:
        obj: SQLAlchemy model instance (e.g., a Youth object)
        _depth: Current recursion depth (internal use for tracking nested relationships)
        max_depth: Maximum recursion depth to prevent infinite loops with circular relationships
    
    Returns:
        Dictionary representation of the SQLAlchemy model suitable for Pydantic
    """
    # Return None if the object is None to handle null relationships
    if obj is None:
        return None
    
    # If we've reached maximum recursion depth, convert the object to a string
    # This prevents infinite recursion with circular relationships (e.g., Youth -> Karyakarta -> Youth)
    if _depth >= max_depth:
        return str(obj)
    
    result = {}
    
    # Iterate through all mapped attributes of the SQLAlchemy model
    # This includes columns and relationships defined in the model
    for key in obj.__mapper__.attrs.keys():
        value = getattr(obj, key)
        
        # Handle case where the value is another SQLAlchemy model (e.g., Youth.karyakarta)
        # This handles single-object relationships like Youth -> Karyakarta
        if hasattr(value, '__mapper__'):
            # Recursively convert the related object, increasing the depth counter
            result[key] = sqlalchemy_to_pydantic_dict(value, _depth + 1, max_depth)

        # Handle case where the value is a collection of SQLAlchemy models
        # This handles one-to-many relationships like Karyakarta -> [Youth1, Youth2, ...]
        elif isinstance(value, (list, set)):
            if value and hasattr(value[0], '__mapper__'):
                result[key] = [
                    sqlalchemy_to_pydantic_dict(item, _depth + 1, max_depth)
                    for item in value
                ]
            else:
                result[key] = list(value)

        # Handle simple attribute values (strings, integers, dates, etc.)
        # This handles regular columns like Youth.first_name, Youth.email, etc.
        else:
            result[key] = value
            
    # Return the complete dictionary representation of the SQLAlchemy model
    return result
