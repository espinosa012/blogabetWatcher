from blogabet import Blogabet as bb

#	Get Blogabet object and login
bb 	=	bb()
bb.blogabet_login()

#	Start watching feed
bb.watch_blogabet_feed(my_tipsters=True)


