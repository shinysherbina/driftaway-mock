import snipJson from "./snipJson.js";
import snipByTag from "./snipByTag.js";

function snipSmart(content, { format = "" } = {}) {
  switch (format) {
    case "json":
      return snipJson(content);

    case "tag":
      return snipByTag(content);

    default:
      return {
        status: "fail",
        comments: "Please choose a format",
        data: null,
        raw: null,
      };
  }
}

export default snipSmart;
