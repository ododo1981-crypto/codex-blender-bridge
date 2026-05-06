const net = require("node:net");

const host = "127.0.0.1";
const port = 9877;

function call(command) {
  return new Promise((resolve, reject) => {
    const client = net.createConnection({ host, port }, () => {
      client.end(JSON.stringify(command));
    });

    const chunks = [];
    client.on("data", (chunk) => chunks.push(chunk));
    client.on("error", reject);
    client.on("end", () => {
      try {
        resolve(JSON.parse(Buffer.concat(chunks).toString("utf8")));
      } catch (error) {
        reject(error);
      }
    });
  });
}

async function main() {
  console.log(await call({ type: "ping", params: {} }));
  console.log(await call({ type: "commands", params: {} }));
  console.log(await call({ type: "status", params: {} }));
  console.log(await call({ type: "get_scene_info", params: { max_objects: 50 } }));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
