const fs = require("fs")
const path = require("path")

const BASE_DIR = __dirname

const folders = [
    "src",
    "src/config",
    "src/controllers",
    "src/middleware",
    "src/models",
    "src/routes",
    "src/services",
    "src/utils",
    "tests"
]

const files = [
    "app.js",
    "server.js",
    "src/config/database.js",
    "src/config/redis.js",
    "src/middleware/auth.middleware.js",
    "src/middleware/error.middleware.js",
    ".env",
    ".env.example",
    ".dockerignore",
    "Dockerfile",
    ".gitignore"
]

function createFolders() {
    folders.forEach(folder => {
        const folderPath = path.join(BASE_DIR, folder)

        if (!fs.existsSync(folderPath)) {
            fs.mkdirSync(folderPath, {
                recursive: true
            })
        }
    })
}

function createFiles() {
    files.forEach(file => {
        const filePath = path.join(BASE_DIR, file)

        if (!fs.existsSync(filePath)) {
            fs.writeFileSync(filePath, "")
        }
    })
}

function createProject() {
    createFolders()
    createFiles()

    console.log("Express MVC structure created successfully")
}

createProject()