" =============================================================================
" Name:         Squirrelsong Dark
" Description:  Low contrast dark theme for web developers.
" URL:          https://github.com/sapegin/squirrelsong/
" License:      MIT
" =============================================================================

" Set to v:false to disable everything but color
let g:squirrelsong_color_only = get(g:, 'squirrelsong_color_only', v:false)

" Initialization: {{
let s:palette = {
  \ 'bg':                  ['#37291d',   'NONE'],
  \ 'blue':                  ['#5094be',   'NONE'],
  \ 'blue_contrast':                  ['#407698',   'NONE'],
  \ 'blue_light':                  ['#59a3d1',   'NONE'],
  \ 'blue_lighter':                  ['#6ac3fa',   'NONE'],
  \ 'bold':                  ['#f4d3b2',   'NONE'],
  \ 'bright_pink':                  ['#de3531',   'NONE'],
  \ 'bright_pink_light':                  ['#ff3f3a',   'NONE'],
  \ 'bright_pink_lighter':                  ['#ff4a44',   'NONE'],
  \ 'bright_yellow':                  ['#e8c138',   'NONE'],
  \ 'bright_yellow_light':                  ['#ffe743',   'NONE'],
  \ 'bright_yellow_lighter':                  ['#ffff4e',   'NONE'],
  \ 'class':                  ['#39968d',   'NONE'],
  \ 'comment':                  ['#6a5d4e',   'NONE'],
  \ 'cursor':                  ['#b29b82',   'NONE'],
  \ 'fg':                  ['#b29b82',   'NONE'],
  \ 'function':                  ['#5094be',   'NONE'],
  \ 'gray04':                  ['#f4d3b2',   'NONE'],
  \ 'gray05':                  ['#d5b89a',   'NONE'],
  \ 'gray07':                  ['#8e7c68',   'NONE'],
  \ 'gray08':                  ['#6a5d4e',   'NONE'],
  \ 'gray09':                  ['#704e35',   'NONE'],
  \ 'gray0a':                  ['#865d3f',   'NONE'],
  \ 'gray0b':                  ['#593e2a',   'NONE'],
  \ 'gray0c':                  ['#423122',   'NONE'],
  \ 'gray0d':                  ['#37291d',   'NONE'],
  \ 'gray0e':                  ['#2c2017',   'NONE'],
  \ 'gray0f':                  ['#211811',   'NONE'],
  \ 'green':                  ['#478332',   'NONE'],
  \ 'green_contrast':                  ['#386828',   'NONE'],
  \ 'green_light':                  ['#669a47',   'NONE'],
  \ 'green_lighter':                  ['#7ab855',   'NONE'],
  \ 'important':                  ['#ba4034',   'NONE'],
  \ 'keyword':                  ['#895eb0',   'NONE'],
  \ 'line':                  ['#593e2a',   'NONE'],
  \ 'number':                  ['#be9e2d',   'NONE'],
  \ 'orange':                  ['#be9e2d',   'NONE'],
  \ 'orange_contrast':                  ['#987e24',   'NONE'],
  \ 'orange_light':                  ['#d0ad32',   'NONE'],
  \ 'orange_lighter':                  ['#ffd43d',   'NONE'],
  \ 'property':                  ['#5094be',   'NONE'],
  \ 'punctuation':                  ['#b29b82',   'NONE'],
  \ 'purple':                  ['#895eb0',   'NONE'],
  \ 'purple_contrast':                  ['#6d4b8c',   'NONE'],
  \ 'purple_light':                  ['#a26fd1',   'NONE'],
  \ 'purple_lighter':                  ['#c285fa',   'NONE'],
  \ 'red':                  ['#ba4034',   'NONE'],
  \ 'red_contrast':                  ['#943329',   'NONE'],
  \ 'red_light':                  ['#de4c3e',   'NONE'],
  \ 'red_lighter':                  ['#ff5b4a',   'NONE'],
  \ 'regexp':                  ['#ba4034',   'NONE'],
  \ 'selection':                  ['#5b3f2b',   'NONE'],
  \ 'string':                  ['#478332',   'NONE'],
  \ 'teal':                  ['#39968d',   'NONE'],
  \ 'teal_contrast':                  ['#2d7870',   'NONE'],
  \ 'teal_light':                  ['#66aba1',   'NONE'],
  \ 'teal_lighter':                  ['#7acdc1',   'NONE'],
  \ 'type':                  ['#39968d',   'NONE'],
  \ 'url':                  ['#59a3d1',   'NONE'],
  \ 'variable':                  ['#5094be',   'NONE'],
  \ 'yellow':                  ['#d4b033',   'NONE'],
  \ 'yellow_contrast':                  ['#a98c28',   'NONE'],
  \ 'yellow_light':                  ['#e8c138',   'NONE'],
  \ 'yellow_lighter':                  ['#ffe743',   'NONE'],
  \ 'none':                  ['NONE',      'NONE']
  \ }

" Apply a highlight style
" @group: The name of the group for the highlight
" @specs: A dictionary with the following keys:
"   @link: A groupname to link this highlight to, other keys are ignored.
"   @fg: An array of two values for guifg and ctermfg, respectively
"   @bg: An array of two values for guibg and ctermbg, respectively
"   @style: A string for special style, e.g.: 'italic', 'bold', 'reverse'
function! s:squirrelsong_hl(group, specs)
  let s:spec_str = ''

  if has_key(a:specs, 'link')
    execute 'highlight! link ' .. a:group .. ' ' .. a:specs['link']
    return
  endif

  if has_key(a:specs, 'fg')
    let s:spec_str = s:spec_str .. ' guifg=' .. a:specs['fg'][0]
    let s:spec_str = s:spec_str .. ' ctermfg=' .. a:specs['fg'][1]
  else
    let s:spec_str = s:spec_str .. ' guifg=NONE'
    let s:spec_str = s:spec_str .. ' ctermfg=NONE'
  endif

  if has_key(a:specs, 'bg')
    let s:spec_str = s:spec_str .. ' guibg=' .. a:specs['bg'][0]
    let s:spec_str = s:spec_str .. ' ctermbg=' .. a:specs['bg'][1]
  else
    let s:spec_str = s:spec_str .. ' guibg=NONE'
    let s:spec_str = s:spec_str .. ' ctermbg=NONE'
  endif

  if !g:squirrelsong_color_only && has_key(a:specs, 'style')
    let s:spec_str = s:spec_str .. ' gui=' .. a:specs['style']
    let s:spec_str = s:spec_str .. ' cterm=' .. a:specs['style']
  else
    let s:spec_str = s:spec_str .. ' gui=NONE'
    let s:spec_str = s:spec_str .. ' cterm=NONE'
  endif

  execute 'highlight' a:group s:spec_str
endfunction

highlight clear
if exists('syntax_on')
  syntax reset
endif

let g:colors_name = 'squirrelsong_dark'
" }}}}

let colors = {}

" Common Highlight Groups {{{{

" UI {{{{
call extend(colors, {
      \ 'Normal':           { 'fg': s:palette.fg, 'bg': s:palette.bg     },
      \ 'Statusline':       { 'fg': s:palette.fg, 'bg': s:palette.gray0a },
      \ 'StatuslineNC':     { 'fg': s:palette.fg, 'bg': s:palette.gray0b },
      \ 'IncSearch':        { 'bg': s:palette.bright_yellow_light },
      \ 'Search':           {  'bg': s:palette.bright_yellow_light },
      \ 'Folded':           { 'fg': s:palette.fg, 'bg': s:palette.gray0a },
      \ 'Visual':           { 'fg': s:palette.none, 'bg': s:palette.bright_yellow_light },
      \ })
" }}}}

" Vanilla Syntax {{{{
call extend(colors, {
      \ 'Type': { 'fg': s:palette.teal, 'style': 'bold' },
      \ 'Structure': { 'fg': s:palette.teal, 'style': 'bold' },
      \ 'StorageClass': { 'fg': s:palette.blue, 'style': 'italic' },
      \ 'Identifier': { 'fg': s:palette.blue, 'style': 'italic' },
      \ 'PreProc': { 'fg': s:palette.red },
      \ 'PreCondit': { 'fg': s:palette.purple },
      \ 'Include': { 'fg': s:palette.purple, 'style': 'bold' },
      \ 'Keyword': { 'fg': s:palette.purple },
      \ 'Define': { 'fg': s:palette.red },
      \ 'Typedef': { 'fg': s:palette.red },
      \ 'Exception': { 'fg': s:palette.red },
      \ 'Conditional': { 'fg': s:palette.purple },
      \ 'Repeat': { 'fg': s:palette.purple },
      \ 'Statement': { 'fg': s:palette.purple },
      \ 'Macro': { 'fg': s:palette.purple },
      \ 'Error': { 'fg': s:palette.red },
      \ 'Label': { 'fg': s:palette.purple },
      \ 'Special': { 'fg': s:palette.purple },
      \ 'SpecialChar': { 'fg': s:palette.purple },
      \ 'Boolean': { 'fg': s:palette.purple },
      \ 'String': { 'fg': s:palette.green },
      \ 'Character': { 'fg': s:palette.orange },
      \ 'Number': { 'fg': s:palette.orange },
      \ 'Float': { 'fg': s:palette.purple },
      \ 'Function': { 'fg': s:palette.blue, 'style':  'bold' },
      \ 'Operator': { 'fg': s:palette.red },
      \ 'Title': { 'fg': s:palette.red, 'style': 'bold' },
      \ 'Tag': { 'fg': s:palette.orange },
      \ 'Delimiter': { 'fg': s:palette.fg },
      \ 'Todo': { 'fg': s:palette.bg, 'bg': s:palette.blue, 'style': 'bold' },
      \ 'Comment': { 'fg': s:palette.comment, 'style': 'italic' },
      \ 'SpecialComment': { 'fg': s:palette.comment, 'style': 'italic' },
      \ 'Ignore': { 'fg': s:palette.gray09 },
      \ 'Underlined': { 'style': 'underline' },
      \ 'Whitespace': { 'fg': s:palette.gray0b },
      \ })

if &diff
  call extend(colors, {
        \ 'CursorLine': { 'style': 'underline' },
        \ 'ColorColumn': { 'style': 'bold' },
        \ })
else
  call extend(colors, {
        \ 'CursorLine': { 'bg': s:palette.gray0b},
        \ 'ColorColumn': { 'bg': s:palette.gray0b },
        \ })
endif
" }}}}

" Predefined Highlight Groups: {{{{
call extend(colors, {
      \ 'Fg': { 'fg': s:palette.fg },
      \ 'Gray': { 'fg': s:palette.gray07 },
      \ 'Red': { 'fg': s:palette.red },
      \ 'Orange': { 'fg': s:palette.orange },
      \ 'Yellow': { 'fg': s:palette.yellow },
      \ 'Green': { 'fg': s:palette.green },
      \ 'Blue': { 'fg': s:palette.blue },
      \ 'Purple': { 'fg': s:palette.purple },
      \ 'Teal': { 'fg': s:palette.teal },
      \
      \ 'RedItalic': { 'fg': s:palette.red, 'style': 'italic' },
      \ 'GrayItalic': { 'fg': s:palette.gray07, 'style': 'italic' },
      \ 'OrangeItalic': { 'fg': s:palette.orange, 'style': 'italic' },
      \ 'YellowItalic': { 'fg': s:palette.yellow, 'style': 'italic' },
      \ 'GreenItalic': { 'fg': s:palette.green, 'style': 'italic' },
      \ 'BlueItalic': { 'fg': s:palette.blue, 'style': 'italic' },
      \ 'PurpleItalic': { 'fg': s:palette.purple, 'style': 'italic' },
      \ 'TealItalic': { 'fg': s:palette.teal, 'style': 'italic' },
      \
      \ 'RedBold': { 'fg': s:palette.red, 'style': 'bold' },
      \ 'GrayBold': { 'fg': s:palette.gray07, 'style': 'bold' },
      \ 'OrangeBold': { 'fg': s:palette.orange, 'style': 'bold' },
      \ 'YellowBold': { 'fg': s:palette.yellow, 'style': 'bold' },
      \ 'GreenBold': { 'fg': s:palette.green, 'style': 'bold' },
      \ 'BlueBold': { 'fg': s:palette.blue, 'style': 'bold' },
      \ 'PurpleBold': { 'fg': s:palette.purple, 'style': 'bold' },
      \ 'TealBold': { 'fg': s:palette.teal, 'style': 'bold' },
      \ })
" }}}}

" }}}}

" Include the rest of your highlight groups here...

for item in items(colors)
  call s:squirrelsong_hl(item[0], item[1])
endfor

" vim: set filetype=vim foldmethod=marker foldmarker={{{{,}}}}:
