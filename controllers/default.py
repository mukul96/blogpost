# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import datetime

def user():
    return dict(form=auth())


@auth.requires_login()
def add_blog_post():
    if request.post_vars['title'] != None:
        blog_title = request.post_vars['title']
        blog_data = request.post_vars['data']
        x = request.post_vars['video']
        y=x.split('=')
        blog_date = datetime.datetime.now()
        db.content.insert(created_by=auth.user.email
                          ,title=blog_title
                        ,data=blog_data
                        ,video='https://www.youtube.com/embed/'+y[1]
                        ,date_time=blog_date)
        redirect(URL('show'))
    return dict()


@auth.requires_login()
def show():
    
    t = request.args(0)
    ids=db().select(db.content.id)
    all_blog={}
    all_comments={}
    all_like=[]
    for row in ids:
        id1 = row.id
        all_blog[id1]={}

        x=db(db.content.id==id1).select(db.content.ALL)
        comments=db(db.comment.blog_id==id1).select(db.comment.ALL)
        likes=db(db.likes.blog_id==id1).select(db.likes.ALL)
        
        
        all_comments[id1]={}
        for i in comments:
            data=i.data
            id2=i.id

            all_comments[id1][id2] = data
        #print all_comments

        for rx in x:
            data = rx.data;
            video=rx.video
            title=rx.title
            created=rx.created_by
        

        x = data;
        z=video
        y=title

        all_blog[id1]['data']=x


        all_blog[id1]['video']=z

        all_blog[id1]['title']=y
        all_blog[id1]['created_by']=created
        h=t
        

        

    return dict(all_blog=all_blog,all_comments=all_comments,y=h)


@auth.requires_login()
def add_comment():
    commented=request.post_vars['commented']
    blog_id=request.post_vars['blog_id']
    db.comment.insert(blog_id=blog_id,data=commented,created_by=auth.user)
    redirect('show')
    
    
    
@auth.requires_login()
def edit_blog():
    title=request.post_vars['title']
    video=request.post_vars['video']
    data=request.post_vars['data']
    blog_id=request.post_vars['blog_id']
    return dict(video=video,data=data,title=title,blog_id=blog_id)


@auth.requires_login()
def edit_show():
    title=request.post_vars['title']
    blog_id=request.post_vars['blog_id']
    data=request.post_vars['data']
    video=request.post_vars['video']
    db(db.content.id==blog_id).update(title=title,data=data,video=video)
    redirect('show')
    
    
@auth.requires_login()
def delete_blog():
    title=request.post_vars['title']
    blog_id=request.post_vars['blog_id']
    data=request.post_vars['data']
    video=request.post_vars['video']
    db(db.content.id==blog_id).delete()
    db(db.comment.blog_id==blog_id).delete()
    redirect('show')
    

@auth.requires_login()
def blog_like():
    blog_id=request.post_vars['blog_id']
    x=0
    if(x==0):
        x=x+1
        session.counter=(session.counter or 0) +1
    else:
        session.counter=session.counter
        
    likes=session.counter
    db.likes.insert(blog_id=blog_id)
    db(db.likes.blog_id==blog_id).update(like=likes)
    redirect(URL('show',args=x))
    
    
@auth.requires_login()
def delete_comment():
    id=request.post_vars['id']
    db(db.comment.id==id).delete()
    redirect('show')
