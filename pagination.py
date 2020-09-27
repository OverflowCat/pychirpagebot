def paginate(title, head, contents, footer, nav_generator):
  pages = []
  for item in contents:
    page = title + head + item + footer
    pages.append[page]
  return pages

