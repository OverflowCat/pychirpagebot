def paginate(title, head, contents, footer, nav_generator):
    return [title + head + item + footer for item in contents]
