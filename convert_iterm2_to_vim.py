import xml.etree.ElementTree as ET
import numpy as np
import os
import sys

# Conversion matrices
P3_TO_XYZ_MATRIX = np.array([
    [0.48657, 0.26567, 0.19823],
    [0.22897, 0.69171, 0.07932],
    [0.00000, 0.04573, 0.95427]
], dtype=np.float32)

# XYZ to sRGB conversion matrix
XYZ_TO_SRGB_MATRIX = np.array([
    [ 3.2406255, -1.5372080, -0.4986286],
    [-0.9689307,  1.8757561,  0.0415560],
    [ 0.0557101, -0.2040211,  1.0572252]
], dtype=np.float32)

# Matrix from example_srgb_p3.py
SRGB_TO_P3_MATRIX = np.array([
    [0.8225, 0.1774, 0],
    [0.0332, 0.9669, 0],
    [0.0171, 0.0724, 0.9108]
], dtype=np.float32)

def p3_to_srgb(r, g, b):
    """Converts P3 RGB to sRGB using NumPy."""
    # First linearize the P3 values (remove gamma)
    p3_linear = np.array([gamma_encode(v) for v in [r, g, b]])
    
    # Convert P3 to XYZ
    xyz_color = np.dot(P3_TO_XYZ_MATRIX, p3_linear)
    
    # Convert XYZ to linear sRGB
    srgb_linear = np.dot(XYZ_TO_SRGB_MATRIX, xyz_color)
    
    # Apply gamma correction to get sRGB
    srgb = np.array([gamma_decode(v) for v in srgb_linear])
    
    # Clamp values to [0,1] range
    srgb = np.clip(srgb, 0.0, 1.0)
    
    return srgb

def srgb_to_p3(r, g, b):
    """Converts sRGB to P3 using proper color space transformation."""
    # First linearize the sRGB values (remove gamma)
    srgb_linear = np.array([gamma_encode(v) for v in [r, g, b]])
    
    # Convert linear sRGB to XYZ
    xyz_color = np.dot(np.linalg.inv(XYZ_TO_SRGB_MATRIX), srgb_linear)
    
    # Convert XYZ to linear P3
    p3_linear = np.dot(np.linalg.inv(P3_TO_XYZ_MATRIX), xyz_color)
    
    # Apply gamma correction to get P3
    p3 = np.array([gamma_decode(v) for v in p3_linear])
    
    # Clamp values to [0,1] range
    p3 = np.clip(p3, 0.0, 1.0)
    
    return p3

def gamma_decode(value):
    """Applies sRGB gamma decoding."""
    if value <= 0.0031308:
        return 12.92 * value
    else:
        return 1.055 * value**(1/2.4) - 0.055

def gamma_encode(value):
    """Applies sRGB gamma encoding (inverse of decoding)."""
    if value <= 0.04045:
        return value / 12.92
    else:
        return ((value + 0.055) / 1.055) ** 2.4

def to_hex(r, g, b):
    """Converts RGB values (0.0-1.0) to hex code."""
    return '#{:02x}{:02x}{:02x}'.format(int(max(0, min(1, r)) * 255),
                                       int(max(0, min(1, g)) * 255),
                                       int(max(0, min(1, b)) * 255))

def convert_color(color, direction='p3_to_srgb'):
    """Convert color between P3 and sRGB color spaces.
    
    Args:
        color: Tuple of (r, g, b) with values in range [0, 1]
        direction: Either 'p3_to_srgb' or 'srgb_to_p3'
        
    Returns:
        Tuple of (r, g, b) in the target color space
    """
    r, g, b = color
    if direction == 'p3_to_srgb':
        return p3_to_srgb(r, g, b)
    elif direction == 'srgb_to_p3':
        return srgb_to_p3(r, g, b)
    else:
        raise ValueError("Direction must be either 'p3_to_srgb' or 'srgb_to_p3'")

def get_color_from_dict(color_dict):
    """Extract RGB color components from an iTerm2 color dictionary."""
    # Find all key/value pairs in the color dictionary
    r, g, b = 0, 0, 0
    is_p3 = False
    
    # Iterate through all children of the dict element in pairs (key, value)
    for i in range(0, len(color_dict) - 1, 2):
        if color_dict[i].tag == 'key':
            key_name = color_dict[i].text
            value_elem = color_dict[i + 1]
            
            if key_name == 'Red Component' and value_elem.tag == 'real':
                r = float(value_elem.text)
            elif key_name == 'Green Component' and value_elem.tag == 'real':
                g = float(value_elem.text)
            elif key_name == 'Blue Component' and value_elem.tag == 'real':
                b = float(value_elem.text)
            elif key_name == 'Color Space' and value_elem.tag == 'string':
                if value_elem.text == 'P3':
                    is_p3 = True
    
    return r, g, b, is_p3

def parse_iterm_colors(iterm_colors_path):
    """Parse iTerm2 colors file and extract colors as sRGB hex values."""
    tree = ET.parse(iterm_colors_path)
    root = tree.getroot()
    
    colors = {}
    
    # Define the mapping between iTerm key names and our Vim palette names
    iterm_to_vim_map = {
        'Ansi 0 Color': 'gray0d',           # Background color equivalent
        'Ansi 8 Color': 'gray09',           # Bright black
        'Ansi 1 Color': 'red',              # Red
        'Ansi 9 Color': 'red_light',        # Bright red
        'Ansi 2 Color': 'green',            # Green
        'Ansi 10 Color': 'green_light',     # Bright green
        'Ansi 3 Color': 'yellow',           # Yellow
        'Ansi 11 Color': 'yellow_light',    # Bright yellow
        'Ansi 4 Color': 'blue',             # Blue
        'Ansi 12 Color': 'blue_light',      # Bright blue
        'Ansi 5 Color': 'purple',           # Magenta
        'Ansi 13 Color': 'purple_light',    # Bright magenta
        'Ansi 6 Color': 'teal',             # Cyan
        'Ansi 14 Color': 'teal_light',      # Bright cyan
        'Ansi 7 Color': 'gray05',           # White
        'Ansi 15 Color': 'gray04',          # Bright white
        'Background Color': 'bg',           # Background
        'Foreground Color': 'fg',           # Foreground
        'Cursor Color': 'cursor',           # Cursor
        'Selection Color': 'selection',     # Selection background
        'Bold Color': 'bold',               # Bold text
    }
    
    # Special colors we'll derive from the existing ones
    derived_colors = {
        'gray0e': ('bg', 0.8),              # Darker background (80% of bg)
        'gray0f': ('bg', 0.6),              # Darkest background (60% of bg)
        'gray0c': ('bg', 1.2),              # Slightly lighter background (120% of bg)
        'gray0b': ('gray09', 0.8),          # Darker bright black
        'gray0a': ('gray09', 1.2),          # Slightly lighter bright black
        'gray07': ('fg', 0.8),              # Darker foreground
        'gray08': ('fg', 0.6),              # Even darker foreground
        'green_lighter': ('green_light', 1.2),
        'green_contrast': ('green', 0.8),
        'teal_lighter': ('teal_light', 1.2),
        'teal_contrast': ('teal', 0.8),
        'blue_lighter': ('blue_light', 1.2),
        'blue_contrast': ('blue', 0.8),
        'purple_lighter': ('purple_light', 1.2),
        'purple_contrast': ('purple', 0.8),
        'red_lighter': ('red_light', 1.2),
        'red_contrast': ('red', 0.8),
        'orange': ('yellow', 0.9),         # Slightly darker yellow
        'orange_light': ('yellow_light', 0.9),
        'orange_lighter': ('yellow_light', 1.1),
        'orange_contrast': ('orange', 0.8),
        'yellow_lighter': ('yellow_light', 1.2),
        'yellow_contrast': ('yellow', 0.8),
        'bright_pink': ('red_light', 1.0, 0.7, 0.8),    # Modified red with more blue
        'bright_pink_light': ('bright_pink', 1.2),
        'bright_pink_lighter': ('bright_pink', 1.4),
        'bright_yellow': ('yellow_light', 1.0),
        'bright_yellow_light': ('yellow_light', 1.2),
        'bright_yellow_lighter': ('yellow_light', 1.4),
        'white': ('#fdfdfe', None),
        'none': ('NONE', None),
    }
    
    # Functional/semantic colors that map to base colors
    semantic_colors = {
        'punctuation': 'fg',
        'comment': 'gray08',
        'keyword': 'purple',
        'number': 'orange',
        'property': 'blue',
        'variable': 'blue',
        'function': 'blue',
        'string': 'green',
        'type': 'teal',
        'class': 'teal',
        'regexp': 'red',
        'important': 'red',
        'url': 'blue_light',
        'line': 'gray0b',
    }
    
    # Parse all colors from the iTerm file
    for key_elem in root.findall('./dict/key'):
        key_name = key_elem.text
        if key_name in iterm_to_vim_map:
            vim_name = iterm_to_vim_map[key_name]
            
            # Find the corresponding dict element (sibling of the key)
            parent = root.find('./dict')
            for i, elem in enumerate(parent):
                if elem is key_elem and i+1 < len(parent) and parent[i+1].tag == 'dict':
                    color_dict = parent[i+1]
                    break
            else:
                continue  # Color dict not found, skip this key
            
            # Get the color components and P3 flag
            r, g, b, is_p3 = get_color_from_dict(color_dict)
            
            # Convert P3 to sRGB if needed
            if is_p3:
                srgb = convert_color((r, g, b), 'p3_to_srgb')
                hex_color = to_hex(*srgb)
            else:
                hex_color = to_hex(r, g, b)
            
            colors[vim_name] = hex_color
    
    # Calculate derived colors
    for derived_name, derived_info in derived_colors.items():
        if derived_info[0] in colors:
            base_color = derived_info[0]
            
            # Handle special case for literal hex values or NONE
            if base_color.startswith('#') or base_color == 'NONE':
                colors[derived_name] = base_color
                continue
                
            # Simple scaling factor
            if len(derived_info) == 2:
                if derived_info[1] is None:  # Special case for fixed values like 'white'
                    colors[derived_name] = base_color
                else:
                    factor = derived_info[1]
                    r_hex = colors[base_color][1:3]
                    g_hex = colors[base_color][3:5]
                    b_hex = colors[base_color][5:7]
                    
                    r = int(r_hex, 16) * factor
                    g = int(g_hex, 16) * factor
                    b = int(b_hex, 16) * factor
                    
                    # Ensure values are in valid range
                    r = max(0, min(255, r))
                    g = max(0, min(255, g))
                    b = max(0, min(255, b))
                    
                    colors[derived_name] = f'#{int(r):02x}{int(g):02x}{int(b):02x}'
            # Custom RGB modifications
            elif len(derived_info) == 4:
                r_factor, g_factor, b_factor = derived_info[1:4]
                r_hex = colors[base_color][1:3]
                g_hex = colors[base_color][3:5]
                b_hex = colors[base_color][5:7]
                
                r = int(r_hex, 16) * r_factor
                g = int(g_hex, 16) * g_factor
                b = int(b_hex, 16) * b_factor
                
                # Ensure values are in valid range
                r = max(0, min(255, r))
                g = max(0, min(255, g))
                b = max(0, min(255, b))
                
                colors[derived_name] = f'#{int(r):02x}{int(g):02x}{int(b):02x}'
    
    # Add semantic colors
    for semantic_name, base_color in semantic_colors.items():
        if base_color in colors:
            colors[semantic_name] = colors[base_color]
    
    return colors

def generate_vim_colorscheme(colors, theme_name):
    """Generate a Vim colorscheme from the color dictionary."""
    # Convert theme name to lowercase with underscores for vim filename
    colors_name = theme_name.lower().replace(" ", "_")
    
    # Start with triple quotes but no trailing backslash
    vim_template = f"""
" =============================================================================
" Name:         {theme_name}
" Description:  Low contrast dark theme for web developers.
" URL:          https://github.com/sapegin/squirrelsong/
" License:      MIT
" =============================================================================

" Set to v:false to disable everything but color
let g:squirrelsong_color_only = get(g:, 'squirrelsong_color_only', v:false)

" Initialization: {{{{
let s:palette = {{
"""
    # Fix: using raw strings to prevent escape sequence warnings
    # Add all colors to the palette
    for i, (color_name, hex_value) in enumerate(sorted(colors.items())):
        # Add comma to all lines except the last one
        comma = "," if i < len(colors) - 1 else ""
        if color_name == 'none':
            vim_template += f"  \\ 'none':                  ['NONE',      'NONE']{comma}\n"
        else:
            vim_template += f"  \\ '{color_name}':                  ['{hex_value}',   'NONE']{comma}\n"
    
    vim_template += r"""
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

let g:colors_name = '""" + colors_name + r"""'
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
"""
    return vim_template

def main():
    # Check for command line arguments
    if len(sys.argv) < 2:
        print("Usage: python scheme.py <iterm_colors_file> [output_vim_file]")
        sys.exit(1)
    
    iterm_colors_path = sys.argv[1]
    
    if not os.path.exists(iterm_colors_path):
        print(f"Error: iTerm colors file '{iterm_colors_path}' not found.")
        sys.exit(1)
    
    # Get the theme name from the file name
    theme_name = os.path.splitext(os.path.basename(iterm_colors_path))[0]
    
    # Set output file path
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        output_path = f"{theme_name.lower().replace(' ', '_')}.vim"
    
    # Parse iTerm colors and generate Vim colorscheme
    colors = parse_iterm_colors(iterm_colors_path)
    vim_colorscheme = generate_vim_colorscheme(colors, theme_name)
    
    # Save the Vim colorscheme
    with open(output_path, 'w') as f:
        f.write(vim_colorscheme)
    
    print(f"Vim colorscheme saved to '{output_path}'")
    
    # Print some example colors for reference
    print("\nExample color conversions:")
    if 'fg' in colors:
        print(f"foreground: {colors['fg']}")
    if 'bg' in colors:
        print(f"background: {colors['bg']}")
    if 'red' in colors:
        print(f"red: {colors['red']}")
    if 'blue' in colors:
        print(f"blue: {colors['blue']}")
    if 'green' in colors:
        print(f"green: {colors['green']}")

if __name__ == "__main__":
    main()
