#!/bin/bash

# create by xia shuang xia
# date: 2016-12-13
# 本程序用于处理时间相关的bash调用
# 可以在本脚本基础上拓展

# 选择起始时间
while [ 1 ]
do
    echo "请输入起始时间距今天的天数:"
    read timecount
    echo "起始时间为: "$(date --date="${timecount} day ago" +%Y-%m-%d)",确定请输入\"y\""
    read y
    if [ ${y} = 'y' -o ${y} = 'Y' -o ${y} = 'Yes' -o ${y} = 'yes' ];then
        break
    fi
done

echo "开始执行脚本..."

let variable=${timecount}+1
while [ 1 ]
do
    if [ ${variable} -eq 0 ]; then
        break;
    else 
        let variable=${variable}-1
    fi

    current=$(date --date="${variable} day ago" +%Y-%m-%d)

    cmd="do something ${current} >> /tmp/${current}.log"

    sleep 1

    # 执行命令
    echo "${current} 正在执行..."
    #`${cmd}`
done

#完成
echo '执行完成...'

