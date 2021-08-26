<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/github_shaishulman/TrendTrackr-app">
    <img src="images/logo.gif" alt="Logo">
  </a>

  <h3 align="center">TrendTrackr App</h3>

  <p align="center">
    Take snapshots of the Twitter trending topics for a specific location (based on Twitter woeid) and provides statistics. 
    <!--
    <br />
    <a href="https://github.com/ShaiShulman/TrendTrackr-app"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/ShaiShulman/TrendTrackr-app">View Demo</a>
    ·
    <a href="https://github.com/ShaiShulman/TrendTrackr-app/issues">Report Bug</a>
    ·
    <a href="https://github.com/ShaiShulman/TrendTrackr-app/issues">Request Feature</a>
    -->
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul> 
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <!--<li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>-->
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Product Name Screen Shot][product-screenshot]

Take snapshots of the trending topics for a specific location, save them on a MongoDB collection and provide history and statistics.
Trending topics are collected from the specified Twitter woeid (location id, translated from string place name) and saved togetehr with sample tweeps for each topic.
The module also provides, command-line form, the history of the collected topics and statistics for each topics (first and last appearances, total volume, ranks, total number days in trending topics)

The main entry point file is trends_app.py 

### Built With

* [Python 3.7](https://www.python.org/)
* [Tweepy](https://www.tweepy.org/)
* [PyMongo](https://pymongo.readthedocs.io/)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Install all prerequisites from the included requirements.txt.

* pip install -r /path/to/requirements.txt

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/github_shaishulman/TrendTrackr-app.git
   ```
2. Install prerequisites
   ```sh
   pip install -r /path/to/requirements.txt
   ```
3. Apply for a standard product Twitter API key
   ```sh
   https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api
   ```

4. Open a free MongoDB user account and get connection string
   ```sh
   https://www.mongodb.com/cloud/atlas/register
   ```

5. Store both Twitter API keys and MongoDB connection string in a file named keys.json (see the included keys_BLANK.json for example)


<!-- USAGE EXAMPLES -->
## Usage

* Save all current trending topics in New York City
   ```sh
   python trends_app.py --save "New York City"
   ```

* Display history of all trending collected since 1 Sep 2021 
   ```sh
   python trends_app.py --date "1/09/2021"
   ```

* Display statistics (first and last appearances, total volume, total number of days) for all topics collected
   ```sh
   python trends_app.py -sta
   ```

* Display dates of being a trending topic for the specific topic "afganistan"
   ```sh
   python trends_app.py --name afganistan
   ```


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Shai Shulman - [@shaishulman](https://twitter.com/shaishulman) - shai.shulman@gmail.com

Project Link: [https://github.com/github_shaishulman/TrendTrackr-app](https://github.com/github_shaishulman/TrendTrackr-app)



<!-- ACKNOWLEDGEMENTS -->
<!--
## Acknowledgements

* []()
* []()
* []()
-->




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ShaiShulman/TrendTrackr-app.svg?style=for-the-badge
[contributors-url]: https://github.com/ShaiShulman/TrendTrackr-app/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ShaiShulman/TrendTrackr-app.svg?style=for-the-badge
[forks-url]: https://github.com/ShaiShulman/TrendTrackr-app/network/members
[stars-shield]: https://img.shields.io/github/stars/ShaiShulman/TrendTrackr-app.svg?style=for-the-badge
[stars-url]: https://github.com/ShaiShulman/TrendTrackr-app/stargazers
[issues-shield]: https://img.shields.io/github/issues/ShaiShulman/TrendTrackr-app.svg?style=for-the-badge
[issues-url]: https://github.com/ShaiShulman/TrendTrackr-app/issues
[license-shield]: https://img.shields.io/github/license/ShaiShulman/TrendTrackr-app.svg?style=for-the-badge
[license-url]: https://github.com/ShaiShulman/TrendTrackr-app/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/shshulman/
[product-screenshot]: images/screenshot.png