import Web3 from "web3";

let web3;

if (typeof window !== "undefined" && typeof window.ethereum !== "undefined") {
  window.ethereum.request({ method: "eth_requestAccounts" }).catch((error) => {
    if (error.code === 4001) {
      window.alert("Connect metamask!");
    } else {
      console.log(error);
    }
  });
  web3 = new Web3(window.ethereum);
  if (!web3) {
    console.log("nope");
  }
} else {
  window.alert("Metamask must be installed to login!");
  web3 = null;
}

export default web3;
