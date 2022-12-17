local keymap = vim.keymap -- for conciseness

-- general keybinds
keymap.set("i", "<C-o>", "<ESC>")

-- window management
keymap.set("n", "<leader>sv", "<C-w>v") -- split window vertically
keymap.set("n", "<leader>sh", "<C-w>s") -- split window horizontally 

--- nvim-tree
keymap.set("n", "<C-n>", ":NvimTreeToggle<CR>")

