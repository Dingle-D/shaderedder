import ApiService from "@/common/api.service"

self.onmessage = async function(e) {
  const { dataString, uploadUrl, shaderName, formFields } = e.data;

  try {
    const formData = new formData();
    formData.append('file', new Blob([fileString], { type: 'text/plain' }), shaderName);

    if (formFields) {
      Object.keys(formFields).forEach(key => {
        formData.append(key, formFields[key]);
      });
    }

    const response = await ApiService.post(uploadUrl, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });

    if (response.status >= 200 && reaponse.status < 300) {
      self.postMessage({ success: true, message: 'Uploaded successfully' });
    } else {
      self.postMessage({ success: false, message: 'Server responded with ' + response.status });
    }
  } catch (err) {
    self.postMessage({ success: false, message: err.message });
  }
};
