export const getUserFromStorage = () => {
    console.log(localStorage.getItem("user"));
    return localStorage.getItem("user") as string;}

export const removeUserFromStorage = () => localStorage.removeItem("user");

export const addUserToStorage = (user: string) =>
  localStorage.setItem("user", user);
