local setup, nvimtree = pcall(require, "nvim-tree")
if not setup then
    return
end

-- recmomended settings
vim.g.loaded = 1
vim.g.loaded_netrwPlugin = 1

vim.cmd([[ highlight NvimTreeIndentMarker guifg=#DA8FF5]])

nvimtree.setup({
    -- change folder arrow icons
    renderer = {
        icons = {
            glyphs = {
                folder = {
                    arrow_closed = "->", -- arrow when folder is closed
                    arrow_open = "v", -- arrow when folder is open
                },
            },
        },
    },
})
