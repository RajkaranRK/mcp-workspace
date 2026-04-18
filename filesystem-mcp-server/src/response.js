export const jsonContent = (value) => ({
  content: [
    {
      type: "text",
      text: JSON.stringify(value, null, 2)
    }
  ]
});
