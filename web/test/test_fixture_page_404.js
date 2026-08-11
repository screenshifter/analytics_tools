import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function contentType(file){
  const ext = path.extname(file).toLowerCase();
  return {
    '.html':'text/html', '.css':'text/css', '.js':'application/javascript', '.json':'application/json', '.png':'image/png', '.jpg':'image/jpeg', '.svg':'image/svg+xml'
  }[ext] || 'application/octet-stream';
}

export function createServer(root = path.join(__dirname, '..', 'build')){
  return http.createServer((req,res)=>{
    let urlPath = decodeURIComponent(req.url.split('?')[0]);
    if (urlPath.includes('..')) { res.writeHead(400); return res.end('Bad request'); }
    let file = path.join(root, urlPath);
    fs.stat(file, (err, st)=>{
      if (!err && st.isDirectory()) file = path.join(file, 'index.html');
      fs.readFile(file, (err2, data)=>{
        if (!err2){
          res.writeHead(200, {'Content-Type': contentType(file)});
          return res.end(data);
        }
        // Not found — serve 404.html if present
        const notFound = path.join(root, '404.html');
        fs.readFile(notFound, (err3, data2)=>{
          if (!err3){
            res.writeHead(404, {'Content-Type':'text/html'});
            return res.end(data2);
          }
          res.writeHead(404, {'Content-Type':'text/plain'});
          res.end('404 Not Found');
        });
      });
    });
  });
}

if (process.argv[1] === __filename){
  const port = process.env.PORT || 8080;
  const root = path.join(__dirname, '..', 'build');
  const server = createServer(root);
  server.listen(port, ()=>console.log(`Serving ${root} on http://localhost:${port}`));
}
