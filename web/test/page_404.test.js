import { beforeAll, afterAll, test, expect } from 'vitest';
import http from 'node:http';
import path from 'node:path';
import { createServer } from './test_fixture_page_404.js';

let server;
let baseUrl;

beforeAll(async () => {
  const root = path.join(process.cwd(), 'build');
  server = createServer(root);
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  const addr = server.address();
  baseUrl = `http://127.0.0.1:${addr.port}`;
});

afterAll(async () => {
  await new Promise((resolve) => server.close(resolve));
});

function httpGet(url){
  return new Promise((resolve, reject) => {
    http.get(url, (res) => {
      let body = '';
      res.on('data', c => body += c);
      res.on('end', () => resolve({ status: res.statusCode, body }));
    }).on('error', reject);
  });
}

test('returns 404 status and 404.html body for unknown paths', async () => {
  const { status, body } = await httpGet(`${baseUrl}/this-path-does-not-exist`);
  expect(status).toBe(404);
  expect(body).toContain('404');
});
