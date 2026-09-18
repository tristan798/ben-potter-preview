# Wraps src/page.html (the artifact fragment) in a full document for static hosting.
import os
here=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(here,'src/page.html'),encoding='utf-8').read()
i=src.index('</style>')+len('</style>')
head=src[:i].replace('<title>Ben Potter</title>','<title>Ben Potter</title>\n<meta name="robots" content="noindex, nofollow">')
open(os.path.join(here,'index.html'),'w',encoding='utf-8').write('<!doctype html>\n<html lang="en-NZ">\n<head>\n'+head+'\n</head>\n<body>'+src[i:]+'\n</body>\n</html>\n')
print('built index.html')
