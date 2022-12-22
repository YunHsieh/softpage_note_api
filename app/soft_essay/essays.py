import uuid

from fastapi import Depends
from fastapi import APIRouter, HTTPException
from app.soft_essay.base_models import (
    Create_Essay, 
    Read_Essays, 
    Query_Essays,
)
from app.soft_essay.models import (
    Softessay_Body,
    Softessay_Essay, 
    Softessay_Topic,
    Softessay_Tag,
)
from app.auth.models import Auth
from app.stores import database
from app.dependencies import get_current_user

router = APIRouter(
    prefix='/essays',
    tags=['items'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/', response_model=list[Read_Essays])
async def read_essays(params: Query_Essays=Depends()):
    return await Softessay_Essay.objects.select_related(
        ['title', 'author', 'forker']
    ).filter(
        **{k: v for k, v in params if v}
    ).all()


@router.post('/', response_model=Softessay_Essay, response_model_exclude_none=True, status_code=201)
async def create_essay(essay: Create_Essay, user: Auth = Depends(get_current_user)):
    async with database.transaction():
        body = essay.dict()
        body['author'] = user
        body['title'], _ = await Softessay_Topic.objects.get_or_create(name=body.pop('title'))
        # HACK: enhance bulk create
        tags = [await Softessay_Tag.objects.get_or_create(name=i) for i in body.pop('tags')]
        essay_instance = await Softessay_Essay(**body).save()
        # HACK: enhance bulk update
        [await essay_instance.tags.add(i) for i, _ in tags]
        contents = essay_instance.content.replace('\n', '\n\@').replace('.', '.\@').split('\@')
        bodies = [await Softessay_Body.objects.get_or_create(essay=essay_instance, content=i) for i in contents if i]
        await essay_instance.update(order_seq=[str(i.id) for i, _ in bodies])
        return essay_instance


@router.get('/{id}', response_model=Read_Essays)
async def read_essay(id: uuid.UUID):
    if not (instance := await Softessay_Essay.objects.select_related(['author', 'title']).get_or_none(id=id)):
        raise HTTPException(404, {'detail': f'No match id: {id}'}) 
    return instance


ResponseBody = Softessay_Body.get_pydantic(
    include={'id', 'content', 'created_at', 'updated_at', 'last_version', 'essay__id'}
)
@router.get('/{essay_id}/contents', response_model=list[ResponseBody])
async def read_content_by_essay(essay_id: uuid.UUID):
    instance = await Softessay_Essay.objects.get_or_none(id=essay_id)
    queryset = await Softessay_Body.objects.select_related('essay').filter(
        last_version=None,
        essay_id=essay_id
    ).all()
    if not instance and not queryset:
        raise HTTPException(404, {'detail': f'No match id: {essay_id}'}) 
    body_dict = {str(i.id): i for i in queryset}
    return [body_dict.get(i) for i in instance.order_seq if i]
