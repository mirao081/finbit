frompathlibimportPath
importio,tokenize

root=Path(r'c:\Users\edu1980\finbit')
text_exts={'.py','.js','.jsx','.ts','.tsx','.css','.scss','.sass','.html','.htm','.xml','.vue','.php'}
exclude_dirs={'.git','.venv','venv','__pycache__','node_modules'}


defstrip_python_comments(path:Path)->bool:
    text=path.read_text(encoding='utf-8',errors='ignore')
try:
        tokens=list(tokenize.generate_tokens(io.StringIO(text).readline))
exceptException:
        returnFalse
new=''.join(tok.stringfortokintokensiftok.type!=tokenize.COMMENT)
ifnew!=text:
        path.write_text(new,encoding='utf-8')
returnTrue
returnFalse


defstrip_css_js_like(text:str)->str:
    out=[]
i=0
n=len(text)
in_string=None
whilei<n:
        ch=text[i]

ifin_stringisnotNone:
            out.append(ch)
ifch=='\\'andi+1<n:
                out.append(text[i+1])
i+=2
continue
ifch==in_string:
                in_string=None
i+=1
continue

ifchin('"',"'",'`'):
            in_string=ch
out.append(ch)
i+=1
continue

iftext.startswith('/*',i):
            j=text.find('*/',i+2)
ifj==-1:
                break
i=j+2
continue

iftext.startswith('//',i):
            prev=text[i-1]ifi>0else''

ifprev==':':
                out.append(ch)
i+=1
continue
j=i+2
whilej<nandtext[j]!='\n':
                j+=1
i=j
continue

iftext.startswith('<!--',i):
            j=text.find('-->',i+4)
ifj==-1:
                break
i=j+3
continue

out.append(ch)
i+=1

return''.join(out)


defstrip_html_comments(text:str)->str:
    out=[]
i=0
n=len(text)
in_tag=False
whilei<n:
        iftext.startswith('<!--',i):
            j=text.find('-->',i+4)
ifj==-1:
                break
i=j+3
continue
out.append(text[i])
i+=1
return''.join(out)

changed=0
forpathinsorted(root.rglob('*')):
    ifnotpath.is_file():
        continue
ifany(partinexclude_dirsforpartinpath.parts):
        continue
ifpath.suffix.lower()notintext_exts:
        continue

text=path.read_text(encoding='utf-8',errors='ignore')
original=text

ifpath.suffix.lower()=='.py':
        new=''.join(tok.stringfortokintokenize.generate_tokens(io.StringIO(text).readline)iftok.type!=tokenize.COMMENT)
elifpath.suffix.lower()in{'.css','.scss','.sass','.js','.jsx','.ts','.tsx'}:
        new=strip_css_js_like(text)
else:
        new=strip_html_comments(text)

ifnew!=original:
        path.write_text(new,encoding='utf-8')
changed+=1

print(f'Updated {changed} files.')
