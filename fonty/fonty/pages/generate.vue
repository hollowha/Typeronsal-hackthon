<template>
  <div class="max-w-6xl mx-auto px-6 py-12 space-y-10 text-gray-800 font-sans">
    <!-- Logo + 標題 -->
    <div class="flex items-center space-x-5 mb-6">
      <img
        src="/typersonal.png"
        alt="Typersonal Logo"
        class="w-32 h-32 object-contain"
      />
      <div>
        <h1
          class="text-4xl font-extrabold tracking-wide leading-tight text-orange-600"
        >
          AI 擴展生成字型
        </h1>
        <p class="text-sm text-gray-500">由字訂藝 Typersonal 提供</p>
      </div>
    </div>

    <!-- 表單區塊 -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
      <!-- 左欄：可輸入多字 -->
      <div class="bg-white rounded-2xl shadow-xl p-6 space-y-6">
        <div>
          <label class="block mb-1 font-semibold text-gray-700"
            >要生成的字（可多個）</label
          >
          <textarea
            v-model="charactersInput"
            class="input min-h-[96px]"
            placeholder="例如：一二三 或 甲乙丙"
          ></textarea>
          <div class="text-xs text-gray-500 mt-1">
            實際字數：{{ uniqueChars.length }}
          </div>
        </div>

        <div>
          <label class="block mb-1 font-semibold text-gray-700"
            >精準度 (Sampling Step)</label
          >
          <input
            v-model.number="samplingStep"
            class="w-full accent-orange-500"
            type="range"
            min="10"
            max="30"
            step="5"
          />
          <div class="text-right text-sm text-gray-500 mt-1">
            目前值：{{ samplingStep }}
          </div>
        </div>

        <div>
          <label class="block mb-1 font-semibold text-gray-700"
            >上傳你的手寫字（PNG）</label
          >
          <input
            type="file"
            accept="image/png"
            @change="onFileChange"
            class="text-sm text-gray-500"
          />
          <p v-if="referenceImage" class="text-xs text-gray-500 mt-1">
            已選擇：{{ referenceImage?.name }}
          </p>
        </div>

        <div class="text-center space-y-3">
          <button
            class="btn-primary w-full max-w-sm"
            :disabled="batching || !referenceImage || uniqueChars.length === 0"
            @click="batchGenerateAndUpload"
          >
            {{
              batching
                ? "處理中… " + doneCount + "/" + uniqueChars.length
                : "批次產生並上傳（PNG → TTF）"
            }}
          </button>
          <div v-if="failures.length" class="text-xs text-red-500">
            有 {{ failures.length }} 個字失敗，可稍後重試。
          </div>
        </div>
      </div>

      <!-- 右欄：預覽與下載 -->
      <div class="bg-white rounded-2xl shadow-xl p-6 space-y-6">
        <div>
          <label class="block mb-1 font-semibold text-gray-700"
            >預覽（已完成）</label
          >
          <div class="grid grid-cols-3 gap-3">
            <div
              v-for="item in results"
              :key="item.filename"
              class="border rounded-lg p-2 text-center"
            >
              <img :src="item.url" class="w-full object-contain rounded" />
              <div class="text-xs text-gray-500 mt-1 break-all">
                {{ item.filename }}
              </div>
            </div>
          </div>
          <div v-if="batching" class="text-sm text-gray-500 mt-2">
            進度：{{ doneCount }}/{{ uniqueChars.length }}
          </div>
        </div>

        <div class="pt-4 border-t text-center">
          <div v-if="ttfUrl">
            <a
              :href="ttfUrl"
              download="fontpico.ttf"
              class="underline text-orange-600 font-semibold"
              >⬇️ 下載 fontpico.ttf</a
            >
          </div>
          <div v-else class="text-sm text-gray-400">
            完成轉換後會顯示下載連結
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import axios from "axios";

// 使用API composable
const { getApiUrl } = useApi();

const charactersInput = ref("一二三");
const samplingStep = ref(15);
const referenceImage = ref(null);
const results = ref([]); // { ch, filename, url, file }
const batching = ref(false);
const doneCount = ref(0);
const failures = ref([]);

const ttfUrl = ref(null);

const uniqueChars = computed(() => {
  const arr = Array.from(charactersInput.value || "").filter(
    (ch) => ch && ch.trim().length
  );
  return Array.from(new Set(arr));
});

function onFileChange(e) {
  const file = e.target.files?.[0] || null;
  if (!file) {
    console.warn("請上傳 PNG 檔");
    return;
  }
  referenceImage.value = file;
}

async function batchGenerateAndUpload() {
  if (!referenceImage.value) {
    console.warn("請先上傳你的手寫字（PNG）");
    return;
  }
  if (uniqueChars.value.length === 0) {
    console.warn("請輸入要生成的字");
    return;
  }

  batching.value = true;
  doneCount.value = 0;
  failures.value = [];
  results.value = [];
  ttfUrl.value = null;

  const generatedFiles = [];

  for (const ch of uniqueChars.value) {
    try {
      const form = new FormData();
      form.append("character", ch);
      form.append("sampling_step", samplingStep.value);
      form.append("reference_image", referenceImage.value);

      const res = await fetch(getApiUrl('/ai/generate'), {
        method: "POST",
        body: form,
      });
      if (!res.ok) throw new Error("模型服務回應失敗");
      const data = await res.json();
      if (!data?.image) throw new Error("缺少 image URL");

      const imgResp = await fetch(data.image);
      if (!imgResp.ok) throw new Error("下載圖片失敗");
      const blob = await imgResp.blob();

      const filename = `${ch.codePointAt(0)}.png`; // 十進位 codePoint 命名
      const file = new File([blob], filename, { type: "image/png" });
      generatedFiles.push(file);

      const url = URL.createObjectURL(blob);
      results.value.push({ ch, filename, url, file });
    } catch (err) {
      console.error("生成失敗：", ch, err);
      failures.value.push(ch);
    } finally {
      doneCount.value += 1;
    }
  }

  if (!generatedFiles.length) {
    batching.value = false;
    console.error("全部字元皆產生失敗，請稍後重試");
    return;
  }

  try {
    const fd = new FormData();
    for (const f of generatedFiles) fd.append("files", f);

    const convertRes = await axios.post("http://localhost:3001/convert", fd, {
      headers: { "Content-Type": "multipart/form-data" },
      responseType: "blob",
    });

    const ttfBlob = new Blob([convertRes.data], {
      type: convertRes.headers["content-type"] || "font/ttf",
    });
    const url = URL.createObjectURL(ttfBlob);
    ttfUrl.value = url;

    // 自動下載
    const a = document.createElement("a");
    a.href = url;
    a.download = "fontpico.ttf";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  } catch (err) {
    console.error("上傳轉檔失敗", err);
    console.error("上傳轉檔失敗，請確認 localhost:3001 是否啟動並允許 CORS");
  } finally {
    batching.value = false;
  }
}

// async function blend() {
//   if (!enableBlend.value || !imageUrl.value) return;

//   try {
//     const blob = await fetch(imageUrl.value).then((res) => res.blob());
//     const form = new FormData();
//     form.append("character", character.value);
//     form.append("style_option", styleOption.value);
//     form.append("alpha", alpha.value);
//     form.append("thickness", thickness.value);
//     form.append("image_a", blob, "image_a.png");

//     const res = await fetch(`${API_BASE_URL}/ai/blend`, {
//       method: "POST",
//       body: form,
//     });
//     if (!res.ok) throw new Error("伺服器回應失敗");
//     const data = await res.json();
//     blendImageUrl.value = data.image;
//   } catch (err) {
//     alert("融合失敗，請稍後重試");
//     console.error("融合失敗", err);
//   }
// }

// async function uploadGeneratedToLocal() {
//   if (!imageUrl.value) {
//     alert("請先產生圖片");
//     return;
//   }
//   ttfLoading.value = true;
//   ttfUrl.value = null;
//   try {
//     // ① 下載模型圖片
//     const resp = await fetch(imageUrl.value);
//     if (!resp.ok) throw new Error("下載生成圖片失敗");
//     const blob = await resp.blob();

//     // ② 用 codePoint 命名，例如 39636.png
//     const filename = `${character.value.codePointAt(0)}.png`;
//     const file = new File([blob], filename, { type: "image/png" });

//     // ③ 依後端 multer 設定（upload.array('files')）上傳
//     const form = new FormData();
//     form.append("files", file);

//     const res = await axios.post("http://localhost:3001/convert", form, {
//       headers: { "Content-Type": "multipart/form-data" },
//       responseType: "blob",
//     });

//     // ④ 取得 TTF Blob 並觸發下載
//     const ttfBlob = new Blob([res.data], {
//       type: res.headers["content-type"] || "font/ttf",
//     });
//     const url = URL.createObjectURL(ttfBlob);
//     ttfUrl.value = url;

//     const a = document.createElement("a");
//     a.href = url;
//     a.download = "fontpico.ttf";
//     document.body.appendChild(a);
//     a.click();
//     document.body.removeChild(a);
//   } catch (e) {
//     console.error(e);
//     alert("轉換失敗：" + e.message);
//   } finally {
//     ttfLoading.value = false;
//   }
// }

// ✅ 當 thickness 調整時，自動即時呼叫 blend（前提是已啟用融合且已有圖）
// watch(thickness, () => {
//   if (enableBlend.value && imageUrl.value) {
//     blend();
//   }
// });
</script>

<style scoped>
.input {
  @apply w-full border border-gray-300 rounded-xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400 transition;
}
.btn-primary {
  @apply bg-orange-500 hover:bg-orange-600 text-white font-bold py-2.5 px-6 rounded-xl transition duration-200 shadow-md;
}
.btn-secondary {
  @apply bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-2.5 px-6 rounded-xl transition duration-200 shadow-md;
}
</style>
