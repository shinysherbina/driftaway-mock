/**
 * Attempts to extract a valid HTML/XML snippet from a given string (e.g., AI response or raw text).
 *
 * Returns the cleaned HTML/XML structure if valid, or a partially extracted snippet if validation fails.
 *
 * @param {string} content - Input string that may contain HTML/XML tags.
 * @param {Object} [options] - Configuration options.
 * @param {boolean} [options.caseSensitive=false] - Whether tag matching is case-sensitive.
 *
 * @returns {Object} result - Result of the parsing attempt.
 * @property {("success"|"fail")} result.status - Indicates if a valid tag structure was found.
 * @property {string} result.comments - Message describing the outcome.
 * @property {string|null} result.data - Extracted valid HTML/XML snippet if successful, otherwise `null`.
 * @property {string|null} result.raw - Partially extracted raw snippet if failed, otherwise `null`.
 *
 * @example
 * const content = "Here is the code you asked for <html><p>Lorem ipsum dolor</p></html>. Feel free to ask more.";
 * const result = snipByTag(content);
 * // result = {
 * //   status: "success",
 * //   comments: "Valid tag structure found",
 * //   data: "<html><p>Lorem ipsum dolor</p></html>",
 * //   raw: null
 * // };
 *
 * See the test cases document for more examples.
 */

function snipByTag(content, { caseSensitive = false } = {}) {
  const result = {
    status: "fail",
    comments: "",
    data: null,
    raw: null,
  };

  if (!content || typeof content !== "string") {
    result.comments = "Invalid input: content must be a string.";
    return result;
  }

  const stack = [];
  let snippetStart = -1;
  let i = 0;

  while (i < content.length) {
    const char = content[i];

    if (char === "<") {
      // Mark where the snippet starts
      if (snippetStart === -1) snippetStart = i;

      let isClosing = false;
      let isSelfClosing = false;
      i++;

      if (content[i] === "/") {
        isClosing = true;
        i++;
      }

      const tagNameStart = i;

      // Extract tag name
      while (i < content.length && /[\w:-]/.test(content[i])) {
        i++;
      }

      const tagNameRaw = content.slice(tagNameStart, i).trim();

      if (tagNameRaw === undefined || tagNameRaw === null) {
        result.comments = "Invalid tag name.";
        result.raw = content.slice(snippetStart, i);
        return result;
      }
      const tagName = caseSensitive ? tagNameRaw : tagNameRaw.toLowerCase();

      // Skip attributes or whitespace
      while (i < content.length && content[i] !== ">") {
        if (content[i] === "/" && content[i + 1] === ">") {
          isSelfClosing = true;
          i += 2;
          break;
        }
        i++;
      }

      if (content[i] === ">") {
        i++; // Skip '>'
      }

      // Process tag type
      if (isClosing) {
        const last = stack.pop();
        if (last !== tagName) {
          result.comments = `Mismatched closing tag: expected </${last}> but found </${tagName}>`;
          result.raw = content.slice(snippetStart, i);
          return result;
        }
      } else if (!isSelfClosing) {
        stack.push(tagName);
      }

      // If all tags closed and stack is empty — success
      if (stack.length === 0 && snippetStart !== -1) {
        result.status = "success";
        result.comments = "Valid tag structure found.";
        result.data = content.slice(snippetStart, i);
        return result;
      }
    } else {
      i++;
    }
  }

  // If we exit the loop and still have unclosed tags
  if (stack.length > 0) {
    result.comments = `Unclosed tag <${stack.pop()}>`;
    result.raw = content.slice(snippetStart);
  } else if (snippetStart !== -1) {
    result.comments = "Incomplete tag structure.";
    result.raw = content.slice(snippetStart);
  } else {
    result.comments = "No tags found.";
  }

  return result;
}

export default snipByTag;
