# surround.nvim

## map
```vim
nmap <Leader>s [surround]
nnoremap <silent> [surround]l :SurroundLine<space>
nnoremap <silent> [surround]w :SurroundWord<space>
nnoremap <silent> [surround]c :ChSurround<space>
nnoremap <silent> [surround]r :RmSurround<CR>
```

## SurroundLine
A state where the cursor is at the second character.  execute `SurroundLine{`.
before
```
def echo(self):
```
after
```
{def echo(self):}
```

## SurroundWord
A state where the cursor is at the second character.  execute `SurroundLine"`.
before
```
def echo(self):
```
after
```
"def" echo(self):
```

## ChSurround
A state where the cursor is at the '('.  execute `ChSurround<`.
before
```
def echo(self):
```
after
```
def echo<self>:
```

## RmSurround
A state where the cursor is at the '('.  execute `RmSurround`.
before
```
def echo(self):
```
after
```
def echoself:
```
