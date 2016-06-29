from chimp import ChimpRequester


a = ChimpRequester()
l = a.get_list("f3984dc96a","test")
l.print_all()
l.insert_all(db)
