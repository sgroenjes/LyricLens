<script setup>
import { ref } from 'vue';
import axios from 'axios';

const artist = ref('');
const songName = ref('');
const lyrics = ref(null);
const lineSentiments = ref(null);
const maxPositiveLine = ref(null);
const maxNegativeLine = ref(null);

function sentimentToColor(sentiment) {
  const adjustedScore = (sentiment + 1) / 2; // Adjust sentiment score from range [-1, 1] to [0, 1]
  const r = adjustedScore < 0.5 ? 255 : Math.floor(255 - ((adjustedScore - 0.5) * 2 * 255));
  const g = adjustedScore > 0.5 ? 255 : Math.floor(adjustedScore * 2 * 255);
  const b = 0;
  return `rgb(${r},${g},${b})`;
}

const submitForm = async () => {
  try {
    const lyricsResponse = await axios.post('/api/lyrics', {
      artist: artist.value,
      song_name: songName.value,
    });
    lyrics.value = lyricsResponse.data.lyrics;

    const sentimentResponse = await axios.post('/api/sentiment', {
      artist: artist.value,
      song_name: songName.value,
    });
    lineSentiments.value = sentimentResponse.data.line_sentiments;
    maxPositiveLine.value = sentimentResponse.data.max_positive_line;
    maxNegativeLine.value = sentimentResponse.data.max_negative_line;
  } catch (error) {
    console.error(error);
    alert('Error fetching data');
  }
};
</script>

<template>

  <main>
    <img alt="Vue logo" class="logo" src="./assets/logo.jpg" width="125" height="125" />
    <h1>LyricLens</h1>
    <form @submit.prevent="submitForm">
      <input v-model="artist" type="text" placeholder="Artist name" required />
      <input v-model="songName" type="text" placeholder="Song name" required />
      <button type="submit">Analyze sentiment</button>
    </form>

    <div v-if="lineSentiments">
      <h2>Lyrics</h2>
      <Popper v-for="(lineSentiment, index) in lineSentiments" :key="index" :content="`Sentiment: ${lineSentiment.sentiment.compound}`">
        <p v-bind:style="{ color: sentimentToColor(lineSentiment.sentiment.compound) }">
          {{ lineSentiment.line }}
        </p>
      </Popper>
    </div>
  </main>
</template>

<style scoped>
:deep(.popper) {
  background: #333;
  padding: 10px;
  border-radius: 4px;
  color: #fff;
  font-size: 13px;
  white-space: nowrap;
}

header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }
}

</style>
