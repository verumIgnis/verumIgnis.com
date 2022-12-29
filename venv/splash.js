const splashTextList = [
  "Made by verumIgnis",
  "ChatGPT is awesome",
  "Tea tastes bad",
  "FAKE NEWS: Not made by ChatGPT!",
  "Open source FTW",
  "NFT = ponzi scheme",
  "Firefox > Chrome",
  "Made by ChatGPT",
  "aluminium NOT aluminum",
  "Protected by cloudflare!",
  "Open source!",
  "github.com/verumIgnis",
  "Troubleshooting...",
  "DAN has no morals",
  "E꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼r꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼r꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼o꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼꙼r꙼꙼꙼꙼",
  "🤡 = 5 min mute in OpenAI",
  "Semicolons are ugly",
  "camelCase > PascalCase",
  "Snek lang is superior",
  "verumIgnis#1564",
  "Chrome eats RAM",
  "This statement is false.",
  "Hosted on a pi4B",
  "Did you know: The earth is round!",
  "Did you know: Vaccines work!",
  "Conspiracy theories are dumb",
  "Did you know: NASA aint here to kill us!",
  "This website sucks",
  "Java has one use",
  "Apple sucks",
  "Adblockers are great",
  "Screw google",
  "Block doubleclick.net",
  "THISisTHEbestCASE"
];

const splashTextElement = document.querySelector('.splashText');

function setRandomSplashText() {
  const randomIndex = Math.floor(Math.random() * splashTextList.length);
  splashTextElement.textContent = splashTextList[randomIndex];
}

setRandomSplashText();
setInterval(setRandomSplashText, 50000);