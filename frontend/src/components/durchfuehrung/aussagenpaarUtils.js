export function getAussageText(item) {
  if (!item) {
    return "";
  }

  if (typeof item === "string") {
    return item;
  }

  return item.aussage ?? "";
}

export function getCorrectValueForPair(aussagenpaar) {
  const aussagen = Array.isArray(aussagenpaar?.aussagen) ? aussagenpaar.aussagen : [];
  const aussageEinsRichtig = Boolean(aussagen[0]?.loesung);
  const aussageZweiRichtig = Boolean(aussagen[1]?.loesung);

  if (!aussageEinsRichtig && !aussageZweiRichtig) {
    return 0;
  }

  if (aussageEinsRichtig && !aussageZweiRichtig) {
    return 1;
  }

  if (!aussageEinsRichtig && aussageZweiRichtig) {
    return 2;
  }

  return 3;
}

function shuffleList(items) {
  const shuffled = [...items];

  for (let index = shuffled.length - 1; index > 0; index -= 1) {
    const swapIndex = Math.floor(Math.random() * (index + 1));
    [shuffled[index], shuffled[swapIndex]] = [shuffled[swapIndex], shuffled[index]];
  }

  return shuffled;
}

function buildPoolFromPairs(aussagenpaare) {
  return aussagenpaare.flatMap((pair) => {
    const aussagen = Array.isArray(pair?.aussagen) ? pair.aussagen : [];
    return aussagen.map((aussage) => ({
      aussage,
      originalPairId: pair.id,
    }));
  });
}

export function buildShuffledKlausurPairs(aussagenpaare, maxAttempts = 400) {
  const statementPool = buildPoolFromPairs(aussagenpaare);

  if (statementPool.length < 2 || statementPool.length % 2 !== 0) {
    return aussagenpaare;
  }

  for (let attempt = 0; attempt < maxAttempts; attempt += 1) {
    const shuffledPool = shuffleList(statementPool);
    const generatedPairs = [];
    let isValid = true;

    for (let index = 0; index < shuffledPool.length; index += 2) {
      const first = shuffledPool[index];
      const second = shuffledPool[index + 1];

      if (!first || !second || first.originalPairId === second.originalPairId) {
        isValid = false;
        break;
      }

      generatedPairs.push({
        id: `klausur-${attempt}-${index / 2}`,
        aussagen: [first.aussage, second.aussage],
        kategorie: [],
        bearbeiter: "",
        grafik_url: "",
        kommentar: "",
      });
    }

    if (isValid) {
      return generatedPairs;
    }
  }

  return aussagenpaare;
}
