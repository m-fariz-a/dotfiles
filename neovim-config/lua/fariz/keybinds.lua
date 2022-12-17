local keymap = vim.keymap -- for conciseness

-- general keybinds
keymap.set("i", "<C-o>", "<ESC>")

-- window management
keymap.set("n", "<leader>sv", "<C-w>v") -- split window vertically
keymap.set("n", "<leader>sh", "<C-w>s") -- split window horizontally 

-- terminal command
keymap.set("n", "<leader>th", ":split | terminal<CR>" ) -- spawn terminal horizontally
keymap.set("n", "<leader>tv", ":vsplit | terminal<CR>" ) -- spawn terminal vertically


