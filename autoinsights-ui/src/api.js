export const analyzeData = async (formData) => {
  const response = await axios.post("http://localhost:8000/api/analyze/", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
  return response.data;
};
