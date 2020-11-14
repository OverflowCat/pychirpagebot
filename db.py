import gspread
gc = gspread.service_account('.gstoken.json')
imgsh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1-R1mFwvI5lxmL4ogJZ64esEQcHZ12sXj1o_KCyoK3rg/edit?usp=drivesdk")

#print(sh.sheet1.get('A1'))
ws = imgsh.sheet1
#ws.append_row(['u','t', 'h', 's'])

def logimg(url, telegraphfileurl, imgid, src, fmt, size):
  ws.append_row([url, telegraphfileurl, imgid, src, fmt, size])