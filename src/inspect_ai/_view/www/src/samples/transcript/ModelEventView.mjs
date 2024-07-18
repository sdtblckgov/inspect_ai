// @ts-check
import { html } from "htm/preact";
import { MetaDataView } from "../../components/MetaDataView.mjs";
import { ChatView } from "../../components/ChatView.mjs";
import { ApplicationIcons } from "../../appearance/Icons.mjs";

/**
 * Renders the StateEventView component.
 *
 * @param {Object} props - The properties passed to the component.
 * @param {import("../../types/log").ModelEvent} props.event - The event object to display.
 * * @param {number} props.index - The index of the event.
 * @returns {import("preact").JSX.Element} The component.
 */
export const ModelEventView = ({ event, index }) => {
  const toolTable = event.tools.reduce((accum, current) => {
    accum[current.name] = current.description;
    return accum;
  }, {});

  const modelProperties = {
    ...event.config,
  };

  if (Object.keys(toolTable).length > 0) {
    modelProperties["tools"] = toolTable;
    modelProperties["tool_choice"] = event.tool_choice;
  }

  if (event.output.usage) {
    modelProperties["usage"] = event.output.usage;
  }

  const outputMessages = event.output.choices.map((choice) => {
    return choice.message;
  });

  return html`
    <div
      style=${{
        display: "grid",
        gridTemplateColumns: "max-content auto",
        columnGap: "0.5em",
      }}
    >
      <div style=${{ fontWeight: 600 }}>
        <i class="${ApplicationIcons.model}" />
      </div>
      <div style=${{ fontWeight: 600 }}>${event.model}</div>
      <div></div>
      <div><${MetaDataView} entries=${modelProperties} compact=${true} /></div>
      <div></div>
      <div>
        <${ChatView}
          id="model-input-${index}"
          messages=${[...event.input, ...outputMessages]}
        />
      </div>
    </div>
  `;
};