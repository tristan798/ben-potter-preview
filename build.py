# Wraps the artifact fragment in a full document for static hosting.
import sys
src=open(sys.argv[1],encoding='utf-8').read()
i=src.index('</style>')+len('</style>')
head=src[:i].replace('<title>Ben Potter</title>','<title>Ben Potter</title>\n<meta name="robots" content="noindex, nofollow">')
open(sys.argv[2],'w',encoding='utf-8').write('<!doctype html>\n<html lang="en-NZ">\n<head>\n'+head+'\n</head>\n<body>'+src[i:]+'\n</body>\n</html>\n')
