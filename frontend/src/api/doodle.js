import API from "./axios";

export const checkBackend = async () => {
  const res = await API.get("/");
  return res.data;
};