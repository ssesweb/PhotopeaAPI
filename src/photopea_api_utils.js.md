// photopea_api_utils.js

/**
 * Opens a PSD file in Photopea.
 * @param {string} fileUrl - The URL of the PSD file.
 * @returns {Promise<void>}
 */
async function openPsdFile(fileUrl) {
    const photopeaUrl = `https://www.photopea.com#%7B%22files%22:%5B%22${encodeURIComponent(fileUrl)}%22%5D%7D`;
    window.open(photopeaUrl, '_blank');
}

/**
 * Closes the current document in Photopea.
 * Note: Photopea API does not have a direct 'close document' function via URL parameters.
 * This function would typically involve sending a script command via Live Messaging if Photopea is embedded in an iframe.
 * For a standalone Photopea instance opened via window.open, closing is usually manual or by closing the tab/window.
 * If Photopea is embedded, you would send a script like `app.activeDocument.close();`
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @returns {void}
 */
function closePsdFile(iframe) {
    if (iframe && iframe.contentWindow) {
        // This assumes Photopea is embedded in an iframe and supports Live Messaging.
        // The script `app.activeDocument.close()` would close the active document.
        // However, direct closing without user interaction might be restricted by browser security policies.
        iframe.contentWindow.postMessage('app.activeDocument.close();', '*');
    } else {
        console.warn("Photopea iframe not found or Live Messaging not applicable for standalone window.");
    }
}

/**
 * Sends a script command to Photopea via Live Messaging.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {string} script - The script string to execute in Photopea.
 * @returns {void}
 */
function sendScriptToPhotopea(iframe, script) {
    if (iframe && iframe.contentWindow) {
        iframe.contentWindow.postMessage(script, '*');
    } else {
        console.error("Photopea iframe not found or invalid.");
    }
}

/**
 * Shows or hides a specific layer in Photopea.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {string} layerName - The name of the layer to show/hide.
 * @param {boolean} visible - True to show, false to hide.
 * @returns {void}
 */
function setLayerVisibility(iframe, layerName, visible) {
    const script = `app.activeDocument.layers.getByName("${layerName}").visible = ${visible};`;
    sendScriptToPhotopea(iframe, script);
}

/**
 * Activates a specific layer in Photopea.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {string} layerName - The name of the layer to activate.
 * @returns {void}
 */
function activateLayer(iframe, layerName) {
    const script = `app.activeDocument.activeLayer = app.activeDocument.layers.getByName("${layerName}");`;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
/**
 * Modifies the text content of a text layer in Photopea.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {string} layerName - The name of the text layer.
 * @param {string} newText - The new text content.
 * @returns {void}
 */
function modifyTextLayer(iframe, layerName, newText) {
    const script = `app.activeDocument.layers.getByName("${layerName}").textItem.contents = "${newText}";`;
    sendScriptToPhotopea(iframe, script);
}

/**
 * Sets the font of a text layer in Photopea.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {string} layerName - The name of the text layer.
 * @param {string} fontName - The name of the font to set.
 * @returns {void}
 */
function setTextLayerFont(iframe, layerName, fontName) {
    const script = `app.activeDocument.layers.getByName("${layerName}").textItem.font = "${fontName}";`;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
/**
 * Replaces the content of a smart object layer with a new image from a URL.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {string} layerName - The name of the smart object layer.
 * @param {string} imageUrl - The URL of the new image.
 * @returns {void}
 */
function replaceSmartObjectImage(iframe, layerName, imageUrl) {
    // This assumes the layer is a Smart Object. For regular pixel layers, a different approach is needed (e.g., deleting and adding a new layer).
    // Photopea's scripting might have a direct way to replace content of a smart object.
    // Based on Photopea's scripting documentation, `app.activeDocument.layers.getByName("LayerName").smartObject.replaceContents(file)` is the method.
    // However, passing a file directly from a URL within the script might be complex due to CORS and file loading.
    // A more robust solution might involve loading the image into Photopea first, then replacing.
    // For simplicity, let's assume a direct script call if Photopea supports it for URLs.
    const script = `
        var layer = app.activeDocument.layers.getByName("${layerName}");
        app.open("${imageUrl}").then(function(newDoc) {
            newDoc.activeLayer.duplicate(layer, ElementPlacement.PLACEATBEGINNING);
            newDoc.close(SaveOptions.DONOTSAVECHANGES);
            layer.remove();
        });
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
/**
 * Exports the current Photopea document to a specified image format and sends it to the OE.
 * Note: This function assumes Photopea is embedded in an iframe and the OE is listening for messages.
 * The actual image data will be sent as an ArrayBuffer message from Photopea.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {string} format - The desired image format (e.g., "png", "jpg", "gif", "psd").
 * @returns {void}
 */
function exportImage(iframe, format) {
    const script = `app.activeDocument.saveToOE("${format}");`;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
/**
 * Retrieves all layer names from the active Photopea document.
 * Note: This function sends a script to Photopea and expects Photopea to echo the result back to the OE.
 * The OE must have a message listener to capture the result.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @returns {void} - The result will be sent back via Live Messaging.
 */
function getAllLayerNames(iframe) {
    const script = `
        var layerNames = [];
        for (var i = 0; i < app.activeDocument.layers.length; i++) {
            layerNames.push(app.activeDocument.layers[i].name);
        }
        app.echoToOE(JSON.stringify(layerNames));
    `;
    sendScriptToPhotopea(iframe, script);
}

/**
 * Retrieves the text content of a specific text layer.
 * Note: Similar to getAllLayerNames, the result is echoed back to the OE.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {string} layerName - The name of the text layer.
 * @returns {void} - The result will be sent back via Live Messaging.
 */
function getTextLayerContent(iframe, layerName) {
    const script = `
        var layer = app.activeDocument.layers.getByName("${layerName}");
        if (layer.kind == LayerKind.TEXT) {
            app.echoToOE(layer.textItem.contents);
        } else {
            app.echoToOE("Layer is not a text layer.");
        }
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
/**
 * Renames a layer in Photopea.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {string} oldName - The current name of the layer.
 * @param {string} newName - The new name for the layer.
 * @returns {void}
 */
function renameLayer(iframe, oldName, newName) {
    const script = `app.activeDocument.layers.getByName("${oldName}").name = "${newName}";`;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
/**
 * Deletes a layer in Photopea.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {string} layerName - The name of the layer to delete.
 * @returns {void}
 */
function deleteLayer(iframe, layerName) {
    const script = `app.activeDocument.layers.getByName("${layerName}").remove();`;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
/**
 * Retrieves font information for a specific text layer.
 * Note: The result is echoed back to the OE.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {string} layerName - The name of the text layer.
 * @returns {void} - The result (JSON string of font info) will be sent back via Live Messaging.
 */
function getLayerFontInfo(iframe, layerName) {
    const script = `
        var layer = app.activeDocument.layers.getByName("${layerName}");
        if (layer.kind == LayerKind.TEXT) {
            var fontInfo = {
                font: layer.textItem.font,
                size: layer.textItem.size,
                color: layer.textItem.color.rgb
            };
            app.echoToOE(JSON.stringify(fontInfo));
        } else {
            app.echoToOE("Layer is not a text layer.");
        }
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
/**
 * Activates a specific document in Photopea by its name.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {string} docName - The name of the document to activate.
 * @returns {void}
 */
function activateDocument(iframe, docName) {
    const script = `app.activeDocument = app.documents.getByName("${docName}");`;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
/**
 * Replaces the content of a frame layer with a new image from a URL.
 * This is similar to replaceSmartObjectImage but specifically for frame layers.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {string} layerName - The name of the frame layer.
 * @param {string} imageUrl - The URL of the new image.
 * @returns {void}
 */
function replaceFrameContent(iframe, layerName, imageUrl) {
    // Assuming Photopea's scripting allows direct replacement for frame layers.
    // The exact script might vary based on Photopea's API for frame layers.
    // A common approach for replacing content in a frame is to use `place` command or similar.
    const script = `
        var layer = app.activeDocument.layers.getByName("${layerName}");
        // This is a placeholder script. Actual Photopea API for frame replacement might differ.
        // You might need to select the frame layer and then use a 'place' command.
        app.activeDocument.activeLayer = layer; // Activate the frame layer
        app.open("${imageUrl}").then(function(newDoc) {
            newDoc.activeLayer.duplicate(layer, ElementPlacement.PLACEATBEGINNING);
            newDoc.close(SaveOptions.DONOTSAVECHANGES);
            layer.remove();
        });
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
/**
 * Replaces the content of a smart object layer with a new image from a URL, with automatic scaling.
 * This function attempts to fit the new image within the bounds of the smart object.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {string} layerName - The name of the smart object layer.
 * @param {string} imageUrl - The URL of the new image.
 * @returns {void}
 */
function replaceSmartObjectImageAndScale(iframe, layerName, imageUrl) {
    const script = `
        var layer = app.activeDocument.layers.getByName("${layerName}");
        app.open("${imageUrl}").then(function(newDoc) {
            var newLayer = newDoc.activeLayer;
            newLayer.duplicate(layer, ElementPlacement.PLACEATBEGINNING);
            newDoc.close(SaveOptions.DONOTSAVECHANGES);

            var bounds1 = layer.bounds;
            var bounds2 = newLayer.bounds;

            var scaleX = (bounds1[2] - bounds1[0]) / (bounds2[2] - bounds2[0]) * 100;
            var scaleY = (bounds1[3] - bounds1[1]) / (bounds2[3] - bounds2[1]) * 100;

            newLayer.resize(scaleX, scaleY, AnchorPosition.MIDDLECENTER);
            newLayer.translate(bounds1[0] - bounds2[0] + (bounds1[2] - bounds1[0])/2 - (bounds2[2] - bounds2[0])/2, bounds1[1] - bounds2[1] + (bounds1[3] - bounds1[1])/2 - (bounds2[3] - bounds2[1])/2);

            layer.remove();
        });
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
/**
 * Sets various formatting properties for a text layer in Photopea.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {string} layerName - The name of the text layer.
 * @param {object} formatProps - An object containing formatting properties (e.g., { size: 24, color: { hex: "#FF0000" }, justification: "center" }).
 * @returns {void}
 */
function setTextLayerFormat(iframe, layerName, formatProps) {
    const script = `
        var layer = app.activeDocument.layers.getByName("${layerName}");
        if (layer.kind == LayerKind.TEXT) {
            var textItem = layer.textItem;
            if (formatProps.size) textItem.size = formatProps.size;
            if (formatProps.color) {
                var newColor = new SolidColor();
                if (formatProps.color.hex) newColor.rgb.hexValue = formatProps.color.hex.substring(1);
                // Add other color formats if needed (e.g., rgb, cmyk)
                textItem.color = newColor;
            }
            if (formatProps.justification) {
                switch (formatProps.justification.toLowerCase()) {
                    case 'left': textItem.justification = Justification.LEFT; break;
                    case 'center': textItem.justification = Justification.CENTER; break;
                    case 'right': textItem.justification = Justification.RIGHT; break;
                    // Add other justifications as needed
                }
            }
            // Add more text properties as needed (e.g., font, leading, tracking, etc.)
        }
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
/**
 * Adds a new image layer to the Photopea document from a URL.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {string} imageUrl - The URL of the image to add.
 * @param {string} [layerName] - Optional name for the new layer.
 * @returns {void}
 */
function addImageLayer(iframe, imageUrl, layerName) {
    const script = `
        app.open("${imageUrl}").then(function(newDoc) {
            var newLayer = newDoc.activeLayer;
            newLayer.duplicate(app.activeDocument, ElementPlacement.PLACEATBEGINNING);
            newDoc.close(SaveOptions.DONOTSAVECHANGES);
            if ("${layerName}" !== "undefined") {
                app.activeDocument.activeLayer.name = "${layerName}";
            }
        });
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
/**
 * Modifies the color of a Solid Color Fill layer.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {string} layerName - The name of the Solid Color Fill layer.
 * @param {string} hexColor - The new color in hexadecimal format (e.g., "#FF0000").
 * @returns {void}
 */
function modifySolidColorFillLayer(iframe, layerName, hexColor) {
    const script = `
        var layer = app.activeDocument.layers.getByName("${layerName}");
        if (layer.kind == LayerKind.SOLIDCOLORFILL) {
            var color = new SolidColor();
            color.rgb.hexValue = "${hexColor.substring(1)}";
            layer.solidColorFill = color;
        }
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
/**
 * Performs a content-aware fill operation in Photopea.
 * This typically requires a selection to be active.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @returns {void}
 */
function contentAwareFill(iframe) {
    const script = `
        app.activeDocument.selection.fillContentAware();
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
/**
 * Retrieves detailed information for all layers in the active Photopea document.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @returns {Promise<Array<object>>} A promise that resolves with an array of layer information objects.
 */
function getAllLayerInfo(iframe) {
    const script = `
        var doc = app.activeDocument;
        var layersInfo = [];
        function getLayerDetails(layer) {
            var info = {
                name: layer.name,
                id: layer.id,
                kind: layer.kind.toString(),
                visible: layer.visible,
                opacity: layer.opacity,
                bounds: layer.bounds.toString(),
                isBackgroundLayer: layer.isBackgroundLayer || false
            };
            if (layer.kind == LayerKind.TEXT) {
                info.text = layer.textItem.contents;
                info.font = layer.textItem.font;
                info.fontSize = layer.textItem.size;
                info.fontColor = layer.textItem.color.rgb.hexValue;
            }
            if (layer.layers) {
                info.children = [];
                for (var i = 0; i < layer.layers.length; i++) {
                    info.children.push(getLayerDetails(layer.layers[i]));
                }
            }
            return info;
        }

        for (var i = 0; i < doc.layers.length; i++) {
            layersInfo.push(getLayerDetails(doc.layers[i]));
        }
        JSON.stringify(layersInfo);
    `;
    return sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
/**
 * Retrieves information for all layer groups in the active Photopea document.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @returns {Promise<Array<object>>} A promise that resolves with an array of layer group information objects.
 */
function getAllLayerGroups(iframe) {
    const script = `
        var doc = app.activeDocument;
        var groupInfo = [];
        function getGroupDetails(layer) {
            if (layer.typename == "LayerSet") {
                var info = {
                    name: layer.name,
                    id: layer.id,
                    visible: layer.visible,
                    opacity: layer.opacity,
                    layers: []
                };
                for (var i = 0; i < layer.layers.length; i++) {
                    info.layers.push({ name: layer.layers[i].name, id: layer.layers[i].id });
                }
                groupInfo.push(info);
            }
            if (layer.layers) {
                for (var i = 0; i < layer.layers.length; i++) {
                    getGroupDetails(layer.layers[i]);
                }
            }
        }

        for (var i = 0; i < doc.layers.length; i++) {
            getGroupDetails(doc.layers[i]);
        }
        JSON.stringify(groupInfo);
    `;
    return sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
/**
 * Retrieves a list of all available fonts in Photopea.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @returns {Promise<Array<string>>} A promise that resolves with an array of font names.
 */
function getAllFonts(iframe) {
    const script = `
        JSON.stringify(app.fonts);
    `;
    return sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
    getAllLayerGroups,
/**
 * Retrieves information for all open documents in Photopea.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @returns {Promise<Array<object>>} A promise that resolves with an array of document information objects.
 */
function getAllDocumentsInfo(iframe) {
    const script = `
        var docsInfo = [];
        for (var i = 0; i < app.documents.length; i++) {
            var doc = app.documents[i];
            docsInfo.push({
                name: doc.name,
                id: doc.id,
                width: doc.width,
                height: doc.height,
                resolution: doc.resolution
            });
        }
        JSON.stringify(docsInfo);
    `;
    return sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
    getAllLayerGroups,
    getAllFonts,
/**
 * Closes the currently active document in Photopea.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {boolean} [saveChanges=false] - Whether to save changes before closing. Defaults to false.
 * @returns {void}
 */
function closeCurrentDocument(iframe, saveChanges = false) {
    const script = `
        if (app.activeDocument) {
            app.activeDocument.close(${saveChanges ? 'SaveOptions.SAVECHANGES' : 'SaveOptions.DONOTSAVECHANGES'});
        }
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
    getAllLayerGroups,
    getAllFonts,
    getAllDocumentsInfo,
/**
 * Saves the currently active Photopea document.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @returns {void}
 */
function saveCurrentDocument(iframe) {
    const script = `
        if (app.activeDocument) {
            app.activeDocument.save();
        }
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
    getAllLayerGroups,
    getAllFonts,
    getAllDocumentsInfo,
    closeCurrentDocument,
/**
 * Retrieves information about the currently active Photopea document.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @returns {Promise<object|null>} A promise that resolves with an object containing document information, or null if no document is active.
 */
function getActiveDocumentInfo(iframe) {
    const script = `
        if (app.activeDocument) {
            JSON.stringify({
                name: app.activeDocument.name,
                id: app.activeDocument.id,
                width: app.activeDocument.width,
                height: app.activeDocument.height,
                resolution: app.activeDocument.resolution
            });
        } else {
            null;
        }
    `;
    return sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
    getAllLayerGroups,
    getAllFonts,
    getAllDocumentsInfo,
    closeCurrentDocument,
    saveCurrentDocument,
/**
 * Retrieves information about the currently active layer in Photopea.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @returns {Promise<object|null>} A promise that resolves with an object containing active layer information, or null if no layer is active.
 */
function getActiveLayerInfo(iframe) {
    const script = `
        if (app.activeDocument && app.activeDocument.activeLayer) {
            var layer = app.activeDocument.activeLayer;
            var info = {
                name: layer.name,
                id: layer.id,
                kind: layer.kind.toString(),
                visible: layer.visible,
                opacity: layer.opacity,
                bounds: layer.bounds.toString(),
                isBackgroundLayer: layer.isBackgroundLayer || false
            };
            if (layer.kind == LayerKind.TEXT) {
                info.text = layer.textItem.contents;
                info.font = layer.textItem.font;
                info.fontSize = layer.textItem.size;
                info.fontColor = layer.textItem.color.rgb.hexValue;
            }
            JSON.stringify(info);
        } else {
            null;
        }
    `;
    return sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
    getAllLayerGroups,
    getAllFonts,
    getAllDocumentsInfo,
    closeCurrentDocument,
    saveCurrentDocument,
    getActiveDocumentInfo,
/**
 * Retrieves detailed information for all layers in the active Photopea document, including nested layers.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @returns {Promise<Array<object>>} A promise that resolves with an array of layer information objects.
 */
function getAllLayersRecursive(iframe) {
    const script = `
        var doc = app.activeDocument;
        var layersInfo = [];

        function getLayerDetailsRecursive(layer) {
            var info = {
                name: layer.name,
                id: layer.id,
                kind: layer.kind.toString(),
                visible: layer.visible,
                opacity: layer.opacity,
                bounds: layer.bounds.toString(),
                isBackgroundLayer: layer.isBackgroundLayer || false
            };

            if (layer.kind == LayerKind.TEXT) {
                info.text = layer.textItem.contents;
                info.font = layer.textItem.font;
                info.fontSize = layer.textItem.size;
                info.fontColor = layer.textItem.color.rgb.hexValue;
            }

            if (layer.layers) { // Check if it's a layer group
                info.children = [];
                for (var i = 0; i < layer.layers.length; i++) {
                    info.children.push(getLayerDetailsRecursive(layer.layers[i]));
                }
            }
            return info;
        }

        for (var i = 0; i < doc.layers.length; i++) {
            layersInfo.push(getLayerDetailsRecursive(doc.layers[i]));
        }
        JSON.stringify(layersInfo);
    `;
    return sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
    getAllLayerGroups,
    getAllFonts,
    getAllDocumentsInfo,
    closeCurrentDocument,
    saveCurrentDocument,
    getActiveDocumentInfo,
    getActiveLayerInfo,
/**
 * Sets the opacity of a specified layer in Photopea.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {string} layerName - The name of the layer to modify.
 * @param {number} opacity - The new opacity value (0-100).
 * @returns {void}
 */
function setLayerOpacity(iframe, layerName, opacity) {
    const script = `
        var layer = app.activeDocument.layers.getByName("${layerName}");
        if (layer) {
            layer.opacity = ${opacity};
        }
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
    getAllLayerGroups,
    getAllFonts,
    getAllDocumentsInfo,
    closeCurrentDocument,
    saveCurrentDocument,
    getActiveDocumentInfo,
    getActiveLayerInfo,
    getAllLayersRecursive,
/**
 * Sets the blend mode of a specified layer in Photopea.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {string} layerName - The name of the layer to modify.
 * @param {string} blendMode - The new blend mode (e.g., "NORMAL", "MULTIPLY", "SCREEN").
 * @returns {void}
 */
function setLayerBlendMode(iframe, layerName, blendMode) {
    const script = `
        var layer = app.activeDocument.layers.getByName("${layerName}");
        if (layer) {
            layer.blendMode = BlendMode.${blendMode.toUpperCase()};
        }
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
    getAllLayerGroups,
    getAllFonts,
    getAllDocumentsInfo,
    closeCurrentDocument,
    saveCurrentDocument,
    getActiveDocumentInfo,
    getActiveLayerInfo,
    getAllLayersRecursive,
    setLayerOpacity,
/**
 * Creates a new document in Photopea.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {object} options - Options for the new document (e.g., { width: 1920, height: 1080, name: "New Document", resolution: 300, fill: "transparent" }).
 * @returns {void}
 */
function createNewDocument(iframe, options) {
    const script = `
        var doc = app.documents.add(
            ${options.width || 1920},
            ${options.height || 1080},
            ${options.resolution || 72},
            "${options.name || 'Untitled-1'}",
            ${options.fill ? `DocumentFill.${options.fill.toUpperCase()}` : 'DocumentFill.TRANSPARENT'}
        );
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
    getAllLayerGroups,
    getAllFonts,
    getAllDocumentsInfo,
    closeCurrentDocument,
    saveCurrentDocument,
    getActiveDocumentInfo,
    getActiveLayerInfo,
    getAllLayersRecursive,
    setLayerOpacity,
    setLayerBlendMode,
/**
 * Resizes the canvas of the active Photopea document.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {number} width - The new width of the canvas.
 * @param {number} height - The new height of the canvas.
 * @param {string} [anchor="MC"] - The anchor point for resizing (e.g., "TL", "MC", "BR").
 * @returns {void}
 */
function resizeCanvas(iframe, width, height, anchor = "MC") {
    const script = `
        if (app.activeDocument) {
            app.activeDocument.resizeCanvas(${width}, ${height}, AnchorPosition.${anchor.toUpperCase()});
        }
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
    getAllLayerGroups,
    getAllFonts,
    getAllDocumentsInfo,
    closeCurrentDocument,
    saveCurrentDocument,
    getActiveDocumentInfo,
    getActiveLayerInfo,
    getAllLayersRecursive,
    setLayerOpacity,
    setLayerBlendMode,
    createNewDocument,
/**
 * Resizes the image of the active Photopea document.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {number} width - The new width of the image.
 * @param {number} height - The new height of the image.
 * @param {string} [resampleMethod="BICUBIC"] - The resampling method (e.g., "BICUBIC", "NEARESTNEIGHBOR").
 * @returns {void}
 */
function resizeImage(iframe, width, height, resampleMethod = "BICUBIC") {
    const script = `
        if (app.activeDocument) {
            app.activeDocument.resizeImage(${width}, ${height}, ResampleMethod.${resampleMethod.toUpperCase()});
        }
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
    getAllLayerGroups,
    getAllFonts,
    getAllDocumentsInfo,
    closeCurrentDocument,
    saveCurrentDocument,
    getActiveDocumentInfo,
    getActiveLayerInfo,
    getAllLayersRecursive,
    setLayerOpacity,
    setLayerBlendMode,
    createNewDocument,
    resizeCanvas,
/**
 * Rotates the canvas of the active Photopea document.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {number} angle - The angle of rotation in degrees.
 * @returns {void}
 */
function rotateCanvas(iframe, angle) {
    const script = `
        if (app.activeDocument) {
            app.activeDocument.rotateCanvas(${angle});
        }
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
    getAllLayerGroups,
    getAllFonts,
    getAllDocumentsInfo,
    closeCurrentDocument,
    saveCurrentDocument,
    getActiveDocumentInfo,
    getActiveLayerInfo,
    getAllLayersRecursive,
    setLayerOpacity,
    setLayerBlendMode,
    createNewDocument,
    resizeCanvas,
    resizeImage,
/**
 * Flips the canvas of the active Photopea document horizontally or vertically.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {string} direction - The direction to flip ("HORIZONTAL" or "VERTICAL").
 * @returns {void}
 */
function flipCanvas(iframe, direction) {
    const script = `
        if (app.activeDocument) {
            if ("${direction.toUpperCase()}" === "HORIZONTAL") {
                app.activeDocument.flipCanvas(Direction.HORIZONTAL);
            } else if ("${direction.toUpperCase()}" === "VERTICAL") {
                app.activeDocument.flipCanvas(Direction.VERTICAL);
            }
        }
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
    getAllLayerGroups,
    getAllFonts,
    getAllDocumentsInfo,
    closeCurrentDocument,
    saveCurrentDocument,
    getActiveDocumentInfo,
    getActiveLayerInfo,
    getAllLayersRecursive,
    setLayerOpacity,
    setLayerBlendMode,
    createNewDocument,
    resizeCanvas,
    resizeImage,
    rotateCanvas,
/**
 * Crops the active Photopea document.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {number} x - The x-coordinate of the top-left corner of the crop area.
 * @param {number} y - The y-coordinate of the top-left corner of the crop area.
 * @param {number} width - The width of the crop area.
 * @param {number} height - The height of the crop area.
 * @returns {void}
 */
function cropDocument(iframe, x, y, width, height) {
    const script = `
        if (app.activeDocument) {
            app.activeDocument.crop(new Bounds(${x}, ${y}, ${x + width}, ${y + height}));
        }
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
    getAllLayerGroups,
    getAllFonts,
    getAllDocumentsInfo,
    closeCurrentDocument,
    saveCurrentDocument,
    getActiveDocumentInfo,
    getActiveLayerInfo,
    getAllLayersRecursive,
    setLayerOpacity,
    setLayerBlendMode,
    createNewDocument,
    resizeCanvas,
    resizeImage,
    rotateCanvas,
    flipCanvas,
/**
 * Adds a layer mask to the active layer in Photopea.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @returns {void}
 */
function addLayerMask(iframe) {
    const script = `
        if (app.activeDocument && app.activeDocument.activeLayer) {
            app.activeDocument.activeLayer.createMask();
        }
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
    getAllLayerGroups,
    getAllFonts,
    getAllDocumentsInfo,
    closeCurrentDocument,
    saveCurrentDocument,
    getActiveDocumentInfo,
    getActiveLayerInfo,
    getAllLayersRecursive,
    setLayerOpacity,
    setLayerBlendMode,
    createNewDocument,
    resizeCanvas,
    resizeImage,
    rotateCanvas,
    flipCanvas,
    cropDocument,
/**
 * Deletes the layer mask from the active layer in Photopea.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @returns {void}
 */
function deleteLayerMask(iframe) {
    const script = `
        if (app.activeDocument && app.activeDocument.activeLayer) {
            app.activeDocument.activeLayer.removeMask();
        }
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
    getAllLayerGroups,
    getAllFonts,
    getAllDocumentsInfo,
    closeCurrentDocument,
    saveCurrentDocument,
    getActiveDocumentInfo,
    getActiveLayerInfo,
    getAllLayersRecursive,
    setLayerOpacity,
    setLayerBlendMode,
    createNewDocument,
    resizeCanvas,
    resizeImage,
    rotateCanvas,
    flipCanvas,
    cropDocument,
    addLayerMask,
/**
 * Applies a filter to the active layer in Photopea.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {string} filterName - The name of the filter to apply (e.g., "GAUSSIAN_BLUR").
 * @param {Array<any>} params - An array of parameters for the filter.
 * @returns {void}
 */
function applyFilter(iframe, filterName, params = []) {
    const script = `
        if (app.activeDocument && app.activeDocument.activeLayer) {
            app.activeDocument.activeLayer.applyFilter(FilterEffect.${filterName.toUpperCase()}, ${JSON.stringify(params)});
        }
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
    getAllLayerGroups,
    getAllFonts,
    getAllDocumentsInfo,
    closeCurrentDocument,
    saveCurrentDocument,
    getActiveDocumentInfo,
    getActiveLayerInfo,
    getAllLayersRecursive,
    setLayerOpacity,
    setLayerBlendMode,
    createNewDocument,
    resizeCanvas,
    resizeImage,
    rotateCanvas,
    flipCanvas,
    cropDocument,
    addLayerMask,
    deleteLayerMask,
/**
 * Adds an adjustment layer to the Photopea document.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @param {string} adjustmentType - The type of adjustment (e.g., "BRIGHTNESSCONTRAST", "CURVES").
 * @param {object} options - An object containing options for the adjustment.
 * @returns {void}
 */
function addAdjustmentLayer(iframe, adjustmentType, options = {}) {
    const script = `
        app.activeDocument.addAdjustmentLayer(AdjustmentLayerType.${adjustmentType.toUpperCase()}, ${JSON.stringify(options)});
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
    getAllLayerGroups,
    getAllFonts,
    getAllDocumentsInfo,
    closeCurrentDocument,
    saveCurrentDocument,
    getActiveDocumentInfo,
    getActiveLayerInfo,
    getAllLayersRecursive,
    setLayerOpacity,
    setLayerBlendMode,
    createNewDocument,
    resizeCanvas,
    resizeImage,
    rotateCanvas,
    flipCanvas,
    cropDocument,
    addLayerMask,
    deleteLayerMask,
    applyFilter,
/**
 * Converts the active layer to a Smart Object in Photopea.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @returns {void}
 */
function convertToSmartObject(iframe) {
    const script = `
        if (app.activeDocument && app.activeDocument.activeLayer) {
            app.activeDocument.activeLayer.convertToSmartObject();
        }
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
    getAllLayerGroups,
    getAllFonts,
    getAllDocumentsInfo,
    closeCurrentDocument,
    saveCurrentDocument,
    getActiveDocumentInfo,
    getActiveLayerInfo,
    getAllLayersRecursive,
    setLayerOpacity,
    setLayerBlendMode,
    createNewDocument,
    resizeCanvas,
    resizeImage,
    rotateCanvas,
    flipCanvas,
    cropDocument,
    addLayerMask,
    deleteLayerMask,
    applyFilter,
    addAdjustmentLayer,
/**
 * Rasterizes the active layer in Photopea.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @returns {void}
 */
function rasterizeLayer(iframe) {
    const script = `
        if (app.activeDocument && app.activeDocument.activeLayer) {
            app.activeDocument.activeLayer.rasterize();
        }
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
    getAllLayerGroups,
    getAllFonts,
    getAllDocumentsInfo,
    closeCurrentDocument,
    saveCurrentDocument,
    getActiveDocumentInfo,
    getActiveLayerInfo,
    getAllLayersRecursive,
    setLayerOpacity,
    setLayerBlendMode,
    createNewDocument,
    resizeCanvas,
    resizeImage,
    rotateCanvas,
    flipCanvas,
    cropDocument,
    addLayerMask,
    deleteLayerMask,
    applyFilter,
    addAdjustmentLayer,
    convertToSmartObject,
/**
 * Merges all visible layers in the active Photopea document.
 * @param {HTMLIFrameElement} iframe - The iframe element containing Photopea.
 * @returns {void}
 */
function mergeVisibleLayers(iframe) {
    const script = `
        if (app.activeDocument) {
            app.activeDocument.mergeVisibleLayers();
        }
    `;
    sendScriptToPhotopea(iframe, script);
}

// Export functions for use in other modules
export {
    openPsdFile,
    closePsdFile,
    setLayerVisibility,
    activateLayer,
    modifyTextLayer,
    setTextLayerFont,
    replaceSmartObjectImage,
    exportImage,
    getAllLayerNames,
    getTextLayerContent,
    renameLayer,
    deleteLayer,
    getLayerFontInfo,
    activateDocument,
    replaceFrameContent,
    replaceSmartObjectImageAndScale,
    setTextLayerFormat,
    addImageLayer,
    modifySolidColorFillLayer,
    contentAwareFill,
    getAllLayerInfo,
    getAllLayerGroups,
    getAllFonts,
    getAllDocumentsInfo,
    closeCurrentDocument,
    saveCurrentDocument,
    getActiveDocumentInfo,
    getActiveLayerInfo,
    getAllLayersRecursive,
    setLayerOpacity,
    setLayerBlendMode,
    createNewDocument,
    resizeCanvas,
    resizeImage,
    rotateCanvas,
    flipCanvas,
    cropDocument,
    addLayerMask,
    deleteLayerMask,
    applyFilter,
    addAdjustmentLayer,
    convertToSmartObject,
    rasterizeLayer,
    mergeVisibleLayers
};