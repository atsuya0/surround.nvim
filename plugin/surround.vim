if exists('g:loaded_surround')
  finish
endif
let g:loaded_surround = 1

command! -nargs=1 SurroundLine call SurroundLine(<f-args>)
command! -nargs=1 SurroundWord call SurroundWord(<f-args>)
command! -nargs=1 ChSurround call ChSurround(<f-args>)
