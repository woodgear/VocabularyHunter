import * as bt from "./browser/tools";
import * as util from "./util";

export default async function initExtenstion() {

    const userIdFromStorage = await bt.getStorage("userId");
    const vhServerFromStorage = await bt.getStorage("vhServer");

    const userIdFromManifest = (await bt.getDevConfig())["userId"];
    const vhServerFromManifest = (await bt.getDevConfig())["vhServer"];

    const userIdNew = util.uuid();
    const vhServerDefault = "http://vocabularyhunter.com";
    const userId = userIdFromManifest || userIdFromStorage || userIdNew;
    const vhServer = vhServerFromManifest || vhServerFromStorage || vhServerDefault;
    await bt.setStorage("userId", userId);
    await bt.setStorage("vhServer", vhServer);

    console.log("userid", userIdFromManifest, userIdFromStorage, userIdNew);

    console.log("vhServer", vhServerFromManifest, vhServerFromStorage, vhServerDefault);

    console.log("init over", userId, vhServer)
    return { userId, vhServer }
}