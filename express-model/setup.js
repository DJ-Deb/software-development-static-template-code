const { execSync } = require("child_process")
const fs = require("fs")

const port = process.argv[2] || "3000"

execSync("npm install express dotenv", {
    stdio: "inherit"
})

execSync("npm install --save-dev nodemon", {
    stdio: "inherit"
})

// Update package.json
const packageJson = JSON.parse(
    fs.readFileSync("package.json", "utf8")
)

packageJson.scripts = {
    ...packageJson.scripts,
    dev: "nodemon server.js",
    start: "node server.js"
}

fs.writeFileSync(
    "package.json",
    JSON.stringify(packageJson, null, 2) + "\n"
)

// Create .env
fs.writeFileSync(
    ".env",
    `PORT=${port}\n`
)

// Create app.js
fs.writeFileSync(
    "app.js",
    `const express = require("express")

const app = express()

app.use(express.json())
app.use(express.urlencoded({ extended: true }))

module.exports = app
`
)

// Create server.js
fs.writeFileSync(
    "server.js",
    `require("dotenv").config()

const app = require("./app")

const PORT = process.env.PORT

app.listen(PORT, () => {
    console.log(\`Server running on port \${PORT}\`)
})
`
)

console.log("Express project setup completed")