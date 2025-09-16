<template>
  <div class="flex flex-col w-full h-full">
    <div ref="editorContainer" class="flex-1">
    </div>
  </div>
</template>

<script setup lang="ts">
  import { onMounted, onUnmounted, watch, ref, toRefs, toRaw } from "vue";
  import * as monaco from "monaco-editor";
  import {useLocalStorage,useResizeObserver,useDebounceFn} from '@vueuse/core'
  import {useGlslMonaco} from "@/composables/useGlslMonaco"

  const props = defineProps<{
    highlightLines: number[],
    content: string
  }>();

  const langId = useGlslMonaco();
  console.log("Glsl identifier: ", langId);

  const emit = defineEmits<(e: "code-change", payload: string) => void>();

  let editorContainer = ref<HTMLElement | null>(null);

  let editor: monaco.editor.IStandaloneEditor;

  let codeStorage = useLocalStorage("codeStorage", "");

  onMounted(() => {
    editor = monaco.editor.create(editorContainer.value as HTMLElement, {
      language: langId,
      theme: "glsl-vs",
      wordBasedSuggestions: false,

      cursorBlinking: "smooth",
      // cursorSmoothCaretAnimation: 'on',

      colorDecorators: true,

      // fontFamily: 'SpaceMono',

      tabSize: 4,

      minimap: {
        enabled: false,
        //side: "left",
        //maxColumn: 80,
      },

      suggest: {
        showInlineDetails: true,
        // @note thanks https://stackoverflow.com/questions/62325624/how-to-allow-completion-suggestions-to-appear-while-inside-a-snippet-in-monaco-e
        snippetsPreventQuickSuggestions: false,
      },

      "semanticHighlighting.enabled": true,
    });

    if (codeStorage.value) {
      editor.setValue(codeStorage.value);
    }

    emit("code-change",
      codeStorage.value
    );

    editor.onDidChangeModelContent(
      useDebounceFn(() => {
        if (codeStorage.value !== editor.getValue()) {
          codeStorage.value = editor.getValue();
          emit("code-change",
            codeStorage.value
          );
          console.log("EMITED CODE CHANGE");
        }
      }, 500)
    );

    console.log(Array.isArray(props.highlightLines));
    console.log("current decorations:", props.highlightLines);
    applyDecorations();   
  });

  let resizer = useResizeObserver(editorContainer, () => {
    editor.layout();
  });

  onUnmounted(() => {
    editor.dispose();
    resizer.stop();
  });

  const currentErrors = ref<number[]>([]);

  watch(() => props.highlightLines, applyDecorations);

  watch(() => props.content, updateStorage);

  function applyDecorations() {
    console.log("applying decorations");
    if (!editor) return;
    
    const decs = props.highlightLines.map(line => ({
      range: new monaco.Range(line, 1, line, 1),
      options: {
        isWholeLine: true,
        className: "error-line"
      }
    }));
    console.log("Decorated:", decs);
    currentErrors.value = editor.deltaDecorations(currentErrors.value, decs);
  }

  function updateStorage() {
    console.log("Update storage executed")
    codeStorage.value = props.content;
    editor.setValue(props.content);
  }

</script>

<style>
.error-line {
  background-color: rgba(255, 0, 0, 0.3); /* светло-красная подложка */
  border-left: 3px solid #ff0000;
}

.error-glyph {
  background: url('data:image/svg+xml;utf8,<svg ...>') no-repeat center center;
  width: 16px;
  height: 16px;
}
</style>

