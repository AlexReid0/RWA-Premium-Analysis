const {Web3} = require('web3');
const axios = require('axios');

axios.get('https://jsonplaceholder.typicode.com/todos/1')
  .then(response => {
    console.log(response.data);
  })
  .catch(error => {
    console.error('Error:', error);
  });

// Function to fetch logs
async function fetchLogs(tokenAddress, apiKey, topic) {
    const url = `https://api.gnosisscan.io/api?module=logs&action=getLogs&address=${tokenAddress}&topic0=${topic}&apikey=${apiKey}`;
    try {
        const response = await axios.get(url);
        return response.data.result;
    } catch (error) {
        console.error(error);
        return null;
    }
}

// Function to fetch transactions for a given token address
async function fetchTransactions(tokenAddress, apiKey) {
    const url = `https://api.gnosisscan.io/api?module=account&action=txlist&address=${tokenAddress}&sort=desc&apikey=${apiKey}`;
    try {
        const response = await axios.get(url);
        return response.data.result;
    } catch (error) {
        console.error(error);
        return null;
    }
}

// Function to fetch ABI
async function fetchAbi(contractAddress, apiKey) {
    const url = `https://api.gnosisscan.io/api?module=contract&action=getabi&address=${contractAddress}&apikey=${apiKey}`;
    try {
        const response = await axios.get(url);
        if (response.data.status === '1') {
            return JSON.parse(response.data.result);
        } else {
            throw new Error('Failed to fetch ABI');
        }
    } catch (error) {
        console.error(error);
        return null;
    }
}

// Function to find event by signature
function findEventBySignature(web3, abi, eventSignatureHash) {
    for (const item of abi) {
        if (item.type === 'event') {
            const signature = `${item.name}(${item.inputs.map(input => input.type).join(',')})`;
            const signatureHash = web3.utils.sha3(signature);
            if (signatureHash === eventSignatureHash) {
                return item;
            }
        }
    }
    return null;
}

// Main function
async function main() {
    const apiKey = 'YOUR_GNOSISSCAN_API_KEY';
    const providerUrl = 'https://YOUR_GNOSIS_RPC_ENDPOINT/';
    const web3 = new Web3(providerUrl);
    const abi = await fetchAbi('0x5c4DE81a9c2b9290315cb6F379D91A49248C6536', apiKey);
    const contractAddress = '0x13385924683d2a2D0ff5D54e3524EbE2D1dE79C3';
    const transactions = await fetchTransactions(contractAddress, apiKey);
    
    let i =0;
    let created = []

    for (const tx of transactions) {
        const receipt = await web3.eth.getTransactionReceipt(tx.hash);

        for (const log of receipt.logs) {
            const eventSignatureHash = log.topics[0];
            const event = findEventBySignature(web3, abi, eventSignatureHash);
            if (event) {
                const decodedLog = web3.eth.abi.decodeLog(event.inputs, log.data, log.topics.slice(1));
                
                if (decodedLog['newContract']){
                    created.push(decodedLog['newContract']);

                }
            } 
        }
    }

    var string = "";
    created.forEach(function(element){
        string += '"'+ element+ '",';
    });
    console.log(string)
    

    
}

main().catch(console.error);



let second_batch = ["0x7ca0118B50432D0A5c69f854FF017B6F22a10f88","0x870cb517bEdE293cdE2593aD97c0316DCea9A36b","0x5a722eda908e3dB61c9a14cCe757Ce673F5e3A17","0x5128828A7A92583eC46cefECB8b4E127ef5F9E2c","0xD54cc5999d383254334926C06405E5B800FfA1Db","0x5D1cdfb3038F25c331feF652F75B3339AC4c52A1","0x14082EEF0e5cCC9d2d36cf627c45f07f3b0A54Dd","0x423cc18b75c8a2331b2abb14d8BaD8DB84635870","0x4bF18196E7689c0bCF60E1Ee81ec5D8F29aD18BD","0x5af2460902bfD79e54926931E61ee03937173beA","0x7d3F9309822a47E41Dd4756dBe162580e2546f33","0xce0eF526bdC57064Fe556a9b2614eEb66608892F","0x69075fE74ea11C5DA9d32AF3D8D6971B11B55D88","0xaB269dcd4a424Cb8fA9432AdC37d021C3D183578","0x4d6876Bd8d2f44d64b13A83a58CeF81860329ef4","0xD1BF0F64EbA2f8BABfdF71DE3e5Cc9E33f97a46A","0x7505ECf9CEF3bC8c34F02BF7547921d2058F3D35","0x988B40198194Ea79Fd650D1c61db996b7dCd0780","0x1a1EC5ef70a643cD35376214E8a8F2eA0d92931D","0x617e80813DA122F0A25e09A731664B5530b8745c","0xEc72022809156FB57564c8C3412e62dBc46298c3","0x0e6A3fa67194ae6594edBE96153E28eeFD2982F0","0xB0Bd62447Ec79ae63407f34D27cB7E536c28179E","0xd0eF2feEef879eB6Ceb23A7809f6bb39e13fF0A8","0x60139f99DDB56b846b998A655DE2d775ACD936a1","0xAee6ded2C8723C1d81d1b5325a2e620Fb055b77b","0x70724f4332D7eE1918f71236c1746CddA732D90a","0x8E1DE7A9fD1B1b2d761a448d63c4429377624843","0xdFDc10a5dbb68d36782A0933678Dc187ec1c2ea4","0x632FaC8692861960b0D928cF6E91FF703eF5C9f5","0xA6662b6c605aFb2cD635b2511eFB10A04a08e79B","0x5a7715Cf01A08FF1903a240c339Fe5e884C01dCf","0x7231CAFCB32D2Ad7072B7beE71Ca9D4e5EBffAfa","0x5f51b44cDBdd5DC9aEcABc2eD80E2b2A8c002866","0xe7e80e20CE71aCd578B18c54382567385771cC37","0xE90e02790f5070Fb89b15863e2dBC3c22532b43E","0x19F824662bA9df78e368022f085B708fccc201c8","0xaE3713AC3717FA539e98618A03e99A68443F5789","0xF552Ac17a396487f233A696bf52B82Bf53080c6d","0x883646e436238811D2ebC309891779DBACb0E917","0x30D0E37Cd8c87153d56E85bb4a45A0AfdB1DF4E5","0x18CC3CE7eD17e47c669982B6C94A0fe2A0b9606e","0x3Fe8DDa02a469043c36a45cA74d624d9362eC2FC","0xfb260178C2c0e5F920aDeA3DcC906BEe4FeA8A27","0x4Df8c0990e1F02810D6A27C452CD70B39F2E0A2C","0x60677266D8BeDD6147e7070ADfD8C681E2d88324","0xcc21B161171B181aA9Cd7226a2C484175AFd1feD","0xBD42A15A05D51158ca3C46CfD26FB19476f91CE6","0x79A956Cf468ee592D6AEf9CE06920989654b1Ce3","0x30107f6F95b946c4ea0eAeB9f7ae436078F971B1","0x90D280b6456F8233e115e6aABb2CA89249DAfD39","0x712d9c2b3077111493B8867C218F0d24A8Aaf059","0x8180C772a3F9b51E127867656aD50704359C9aa7","0xb061E8dA0b08c8647516921AF6a49B81D425f09F","0x39479370B7FA2c944F6868CA59e191352D2C7111","0x5D0f382a64AcB0ffF716bF2f786b9df4DC8DAD0C","0x16b18B9836Fd01f1413b1bca28935aC00A1f43cE","0x80EFfD75fa30B8b89997D2522b3283A1e768F1bC","0x53279E01efDA8c67404CE98462B831611D5DCca2","0x80d2956433A1622c336480Ba5357350A30644c0a","0x72f1D0719D8Ce0B03d35DEF98e5DBb17854aB285","0x140d6CfDe793f1A2EeD5274454aa6f463EC8C075","0xc2fB83F45C53d2194a9Ee82E4Bda3EE2120141f5","0x9dfD50Ac7CB60832bf7b1C7C46204eFcbd2cc959","0x2010c480B73fD0865b6d2f164660Da852d178d5D","0x7318C373695F8f3C8987A158d41D65EeD4bADb25","0x969e3E55C8A4D9C4cd5E2660a2000ae12aAd9E3E","0x22C9F21F3Be50863997e4E2e4F8F2686BE79Ec93","0x3f8EcB2D158CDE11587270aB3f9744E0f3108354","0x2C12648dfA8d69C441b6b308c7d76661c1e6D1E7","0x14b0d23238c5277f8243d2739c005480D8022fE0","0x053B0BD329dc21Bd4fa278F62310f668c5f1A6ed","0x34A1A58dE8Ff7Ea0A690888D9b8Ae646a8480fA4","0x4326972a016D707c5c6bc854398AaBb6780C62e9","0xf96BcF8a5d9Fa5258BCf243FeB43500a2174ABD6","0x8f0ef86eFe4F2Eba5F7a7bf4D0F3b6BC5681a7A7","0x2B86741b2fBb1DDB8e7387965Cf22eC656a38Dc1","0xb87798476389475CBc96d63aA801b7D25c50d5f1","0x3C20f694Df207eDd49408cf722898bc9002287B9","0x56aa13DD3b1e3f6EC9281b36ce2fe943A217ceB4","0xc38e84bCC2D2693dD77d89F2b86a83e7fE98AFa5","0x1Cc42015d1E4C97D8739D8fE663c47F0a49E9A38","0x1676c0026D714dcCb536e69b3Ae6F46d150e0F26","0xc4A58F3746663bC22A0DA17846B5F9C6B8Ab4876","0x9dFaa0B7B69F39632AD514CFaBA2997cf5B58360","0xDD79587C22D7b2A68c0AA0752a6F83B1d77556CD","0xc49297C99F880f5F19Df4aC988EbA4DF03ef6333","0x40074c412154562fb16441106c95900467E9C173","0x01b4eA64E4204b51cbc8463FFC8e6046C9D70371","0xe4c74C3852cb088e49a010fB0B79159859623Da2","0xd018C66416f3fb6e96f1AD2A758677e1E019E3FB","0x67f685A20FB55aC5e7d128d66a13bdBe77599136","0x550A0C95Fe1762D9cb553402ccC65BcD71594692","0x4637aa1A13Aa4050C6E4bCd6ddE9c39E80E9dD54","0x19D01C13e6e5A1A990dB9821358a591583F63234","0x5c001CcC6340421590a200A328b1d7fC7D454964","0x02B5d51E29Fa35C9228cFa3ff968DA6AaF1048dd","0x20c1216E14cb307A0987EAeaE4b7c7f3888aD538","0xCb2928D422CC2f349Bfb67ee74113a3101a58cb4","0x5CC180BF9091a2284624567ee3c5a2A465656301","0x92ea0f03b611E7e6D056371a3c6B2Bb188199C47","0x7804e5ae01bb68e5a07A40b109EcE66a66772d5E","0x717bfbFa88859Ac34F9772D92749C4B384C6B479","0xD63265bbE136Deff4F26e5976d21840C25DF5E7a","0x3e98281a3dc794799159732D5a488e6cEA645C37","0xD8B9c3c10ba1d9f926b94b45859B65B2900e49bB","0x8236067c1b6Dc176EBdA95531168e93bBCEe25b0","0x60888b47Eb7290EaA8823568FCFFA17Da1A853D9","0x6c76cB9Ff41B40F75Fe8424268370A6c58f8468a","0x032F0e16B729210551642F3249F6e0B1b52A63BE","0xF9A932DF2010bD3d0e0f47Bc61b7104aB82874dA","0x591882dC0581A69f377dF4CaD2CeE4E9855ef34D","0x9aFDd1e3EEc7985b9Dcc3dA1ed030498ea031a6C","0xb5fb9e224A5Cc76E61928eA7985d251520a5579c","0x47a544a460ED29D6622A6f6E68De7f873Cc30e67","0x820629dB01bB56A62Bc75aEeF6EB8dfb0Eec1d04","0xA9e20a86d66493FD146abb9A1f946864773Ce0ae","0x016E0081FcAad345691027908D5044534BcA1946","0x6F0E040d9F02830c6eea5b287AD74369a9E5F1E1","0x7524d382373c1a091789978A8b2C1DC707D2B213","0xB7c1C306bFf953dF8997cC8D91949B7AFf36772b","0x86b4f8135A39DC349A963969F33C3D030726cf61","0x88F37cEE57B669CC1557D4f353dC11c113873F0B","0x1d9Fd5c3FbFd4758F22438a336068b813872cEfC","0x12413a603d16893D8F406925289f206b3B974Cf0","0x0c84153FDcAfd65a4536c2d8d4856E6a6457fB21","0x2F5BB131614d6C2BE8520E355752576Ad55416B4","0x3AC16e7177a55D5fd8F8aB58263D1c764D462fDE","0x458b169D6D9D5d021d61013E3A01bF7dee29DD90","0x70bE90cD788bEf69d52b0D6E767EFE3b289bd0B4","0x296499543eDa4aa175bB9C1464629e94af8de0EA"]

print(len(second_batch));