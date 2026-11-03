import WebSocket from 'ws';
const wsUrl = 'wss://stream.binance.com:9443/ws/btcusdt@kline_1m';
const ws = new WebSocket(wsUrl);

ws.onopen = () => {
  console.log('WebSocket connected');
  const subscribeMsg = {
    method: "SUBSCRIBE",
    params: ["btcusdt@kline_1m"],
    id: Date.now() // 使用唯一 ID 避免重复
  };
  console.log('Sending subscribe message:', subscribeMsg);
  ws.send(JSON.stringify(subscribeMsg));
};

ws.onmessage = (event) => {
  console.log('Message received:', event.data);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('WebSocket closed');
};
