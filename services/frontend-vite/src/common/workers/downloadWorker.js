import axios from 'axios'

self.addEventListener('message', async (event) => {
  const { url } = event.data;

  try {
    const response = await axios.get(url, {
      responseType: 'blob',
    });
    const blob = response.data;
    self.postMessage({ success: true, data: blob});
  } catch (error) {
    self.postMessage({ success: false, data: null, error });
  }
})
