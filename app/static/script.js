
const swiper = document.querySelector('#swiper');
const like = document.querySelector('#like');
const dislike = document.querySelector('#dislike');

const getAnime= async() => {
    const url= "https://api.jikan.moe/v4/anime"
    const res= await fetch(url)
    const data= await res.json()
    const animes = data.data
    for (let i = 0; i < animes.length; i++) {
        appendNewCard(i,animes);
      }
}

const likeAnime = async(anime) => {
    const url = "/like"
    const options = {
        method: "POST",
        headers:{
            "content-type": "application/json"
        },
        body: JSON.stringify({
            user: document.getElementById("user_id").innerText, anime: anime.title
        })
    }
    const res = await fetch(url, options)
    const data = await res.json()
    console.log(data)
}

function appendNewCard(index,animes) {
  const card = new Card({
    imageUrl: animes[index].images.jpg.image_url,
    onDismiss: () => {appendNewCard(index,animes)},
    onLike: () => {
      like.style.animationPlayState = 'running';
      like.classList.toggle('trigger');
      //Make Post request to /likes
      likeAnime(animes[index])
    },
    onDislike: () => {
      dislike.style.animationPlayState = 'running';
      dislike.classList.toggle('trigger');
    }
  });
  swiper.append(card.element);
  

  const cards = swiper.querySelectorAll('.card:not(.dismissing)');
  cards.forEach((card, index) => {
    card.style.setProperty('--i', index);
  });
}

getAnime()