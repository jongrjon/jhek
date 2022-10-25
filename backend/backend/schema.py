from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
import blog.models
import cv.models
import graphene

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class AuthorType(DjangoObjectType):
    class Meta:
        model = blog.models.Profile

class PostType(DjangoObjectType):
    class Meta:
        model = blog.models.Post

class TagType(DjangoObjectType):
    class Meta:
        model = blog.models.Tag

class PersonType(DjangoObjectType):
    class Meta:
        model = cv.models.Person

class CVItemType(DjangoObjectType):
    class Meta:
        model = cv.models.CVItem

class SkillType(DjangoObjectType):
    class Meta:
        model = cv.models.Skill

class ReccommendorType(DjangoObjectType):
    class Meta:
        model = cv.models.Reccommendor

class ItemPointType(DjangoObjectType):
    class Meta:
        model = cv.models.ItemPoint

class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    author_by_username = graphene.Field(AuthorType, username=graphene.String())
    post_by_slug = graphene.Field(PostType, slug=graphene.String())
    posts_by_author = graphene.List(PostType, username=graphene.String())
    posts_by_tag = graphene.List(PostType, tag=graphene.String())
    all_persons = graphene.List(PersonType)
    all_skills = graphene.List(SkillType)
    all_reccomendors = graphene.List(ReccommendorType)
    all_items = graphene.List(CVItemType)
        
    def resolve_all_posts(root, info):
        return (
            blog.models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .all()
        )
    
    def resolve_author_by_username(root, info, username):
        return blog.models.Profile.objects.select_related("user").get(
            user__username=username
         )

    def resolve_post_by_slug(root, info, slug):
        return (
            blog.models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .get(slug=slug)
        )

    def resolve_posts_by_author(root, info, username):
        return (
            blog.models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .filter(author__user__username=username)
        )

    def resolve_posts_by_tag(root, info, tag):
        return (
            blog.models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .filter(tags__name__iexact=tag)
        )

    def resolve_all_persons(root,info):
        return(
            cv.models.Person.objects
            .all()
        )

    def resolve_all_skills(root,info):
        return(
            cv.models.Skill.objects
            .all()
        )

    def resolve_all_reccomendors(root,info):
        return(
            cv.models.Reccommendor.objects
            .all()
        )

    def resolve_all_items(root,info):
        return(
            cv.models.CVItem.objects
            .all()
        )

schema = graphene.Schema(query=Query)
