# app/crud/base_crud.py
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
# from sqlalchemy.orm import Session # Example if using SQLAlchemy

# Define ModelType, CreateSchemaType, UpdateSchemaType
ModelType = TypeVar("ModelType", bound=BaseModel) # Would be SQLAlchemy model
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

# This is a very basic stub. A real CRUD base would interact with a database.
# For now, it will use an in-memory dictionary.

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A Pydantic model (or SQLAlchemy model in a real app) class
        """
        self.model = model
        self._db: Dict[UUID, ModelType] = {} # In-memory store

    def get(self, item_id: Union[UUID, str]) -> Optional[ModelType]:
        # In a real app: db_session: Session
        # return db_session.query(self.model).filter(self.model.id == item_id).first()
        return self._db.get(UUID(str(item_id)))

    def get_multi(
        self, *, skip: int = 0, limit: int = 100, **filters: Any
    ) -> List[ModelType]:
        # In a real app: db_session: Session
        # query = db_session.query(self.model)
        # for field, value in filters.items():
        #     if hasattr(self.model, field) and value is not None:
        #         query = query.filter(getattr(self.model, field) == value)
        # return query.offset(skip).limit(limit).all()
        
        all_items = list(self._db.values())
        # Basic filtering (can be expanded)
        filtered_items = []
        for item in all_items:
            match = True
            for key, value in filters.items():
                if hasattr(item, key) and getattr(item, key) != value:
                    match = False
                    break
            if match:
                filtered_items.append(item)
        return filtered_items[skip : skip + limit]

    def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        # In a real app: db_session: Session
        # obj_in_data = jsonable_encoder(obj_in)
        # db_obj = self.model(**obj_in_data)  # type: ignore
        # db_session.add(db_obj)
        # db_session.commit()
        # db_session.refresh(db_obj)
        # return db_obj
        
        # For Pydantic models, ensure 'id' is part of the model if not handled by BaseUUIDModel
        obj_data = obj_in.model_dump()
        if 'id' not in obj_data or obj_data.get('id') is None:
             obj_data['id'] = uuid.uuid4()

        # Simulate creation by passing all fields from CreateSchemaType
        # and adding default_factory fields if not present
        db_obj = self.model(**obj_data)
        self._db[db_obj.id] = db_obj
        return db_obj

    def update(
        self,
        item_id: Union[UUID, str],
        *,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> Optional[ModelType]:
        # In a real app: db_session: Session
        # db_obj = db_session.get(self.model, item_id) # SQLAlchemy 2.0+
        # if not db_obj:
        #     return None
        # obj_data = jsonable_encoder(db_obj)
        # if isinstance(obj_in, dict):
        #     update_data = obj_in
        # else:
        #     update_data = obj_in.model_dump(exclude_unset=True)
        # for field in obj_data:
        #     if field in update_data:
        #         setattr(db_obj, field, update_data[field])
        # db_session.add(db_obj)
        # db_session.commit()
        # db_session.refresh(db_obj)
        # return db_obj
        db_obj = self._db.get(UUID(str(item_id)))
        if not db_obj:
            return None
        
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)
        
        updated_item = db_obj.model_copy(update=update_data)
        self._db[db_obj.id] = updated_item
        return updated_item


    def remove(self, *, item_id: Union[UUID, str]) -> Optional[ModelType]:
        # In a real app: db_session: Session
        # obj = db_session.get(self.model, item_id)
        # if obj:
        #     db_session.delete(obj)
        #     db_session.commit()
        # return obj
        return self._db.pop(UUID(str(item_id)), None)

